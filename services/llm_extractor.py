"""
LLM Field Extractor — Phi-3.5-mini-instruct via llama-cpp-python.
Model loaded once at import time. GGUF auto-downloaded on first run.
"""

import json
import os
import re
import time

from huggingface_hub import hf_hub_download
from llama_cpp import Llama

# --- Model config ---
_REPO = "bartowski/Phi-3.5-mini-instruct-GGUF"
_FILE = "Phi-3.5-mini-instruct-Q4_K_M.gguf"

_SYSTEM_PROMPT = """You extract personal data from Moroccan CNIE card OCR output.

FIELDS:
- last_name_fr / last_name_ar: family name (French UPPERCASE)
- first_name_fr / first_name_ar: given name (French UPPERCASE)
- birth_date: DD.MM.YYYY
- birth_place_fr: city UPPERCASE
- birth_place_ar: correct Arabic for the city (translate from French, don't copy OCR)
- expiry_date: DD.MM.YYYY
- card_number: letters + digits
- gender: M or F

RULES:
- French text is more reliable than Arabic for names/places
- Fix OCR errors: 1→I, 0→O, 7→T in names/places
- Return null (not "null") for missing fields
- Return ONLY valid JSON, no explanation."""

# --- Load model at import time ---
print("Downloading Phi-3.5-mini GGUF (first run only)...")
_t0 = time.time()
_model_path = hf_hub_download(repo_id=_REPO, filename=_FILE)
print(f"Model ready ({time.time() - _t0:.1f}s)")

_n_threads = os.cpu_count() or 4
print(f"Loading Phi-3.5-mini with {_n_threads} threads...")
_t0 = time.time()
_llm = Llama(
    model_path=_model_path,
    n_ctx=2048,
    n_threads=_n_threads,
    verbose=False,
)
print(f"LLM loaded ({time.time() - _t0:.1f}s)")


def _format_detections(detections):
    """Format filtered OCR detections into text for the LLM."""
    lines = ["OCR detections:"]
    for d in detections:
        lines.append(f"  - text: '{d['text']}', confidence: {d['confidence']}")
    return "\n".join(lines)


def _parse_json(raw):
    """Extract JSON from LLM response, handling wrapper text."""
    cleaned = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()
    # Try full string first, then regex extraction
    for candidate in [
        cleaned,
        re.search(r"\{[^{}]*\}", cleaned, re.DOTALL),
        re.search(r"\{.*\}", cleaned, re.DOTALL),
    ]:
        try:
            txt = candidate.group() if hasattr(candidate, "group") else candidate
            if txt:
                return json.loads(txt)
        except (json.JSONDecodeError, AttributeError):
            continue
    return None


def extract_fields(detections):
    """
    Run LLM extraction on filtered OCR detections.

    Args:
        detections: list of {"text": str, "confidence": float}
                    (should already be filtered by template_filter)

    Returns:
        dict with:
            - fields: dict of extracted fields (or None on failure)
            - time_ms: float
            - tokens_in: int
            - tokens_out: int
            - raw: str (raw LLM output for debugging)
    """
    ocr_text = _format_detections(detections)

    t0 = time.time()
    response = _llm.create_chat_completion(
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": f"Extract fields:\n\n{ocr_text}"},
        ],
        response_format={"type": "json_object"},
        max_tokens=512,
        temperature=0.1,
    )
    elapsed_ms = (time.time() - t0) * 1000

    raw = response["choices"][0]["message"]["content"]
    usage = response.get("usage", {})

    fields = _parse_json(raw)

    return {
        "fields": fields,
        "time_ms": round(elapsed_ms, 1),
        "tokens_in": usage.get("prompt_tokens", 0),
        "tokens_out": usage.get("completion_tokens", 0),
        "raw": raw,
    }
