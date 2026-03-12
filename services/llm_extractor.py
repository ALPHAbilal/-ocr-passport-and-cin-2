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

# Original notebook prompt (9/10) with surgical fixes:
# - "Copy exactly" added (model was translating Arabic↔French)
# - "French more reliable" removed (caused model to skip Arabic)
# - Expanded IGNORE list (OCR variants seen in production)
_SYSTEM_PROMPT = """You extract personal data from Moroccan CNIE card OCR output.



NAMES: the card contains frensh and arabic of the same person so extract them in both language and as they are should be preserved from the input that you will recive next.

OTHER FIELDS:
- birth_date: DD.MM.YYYY
- birth_place_fr: place where it born in frensh
- birth_place_ar: place where it born in arabic
- expiry_date: DD.MM.YYYY
- card_number: 1-2 letters + 5-6 digits
- gender: M or F

RULES:
- Fix OCR errors: 1→I, 0→O, 7→T in names/places
- Return ONLY JSON, no explanation.

Example output:
{"last_name_fr": "ALAOUI", "first_name_fr": "MOHAMMED", "last_name_ar": "العلوي", "first_name_ar": "محمد", "birth_date": "15.06.1990", "birth_place_fr": "CASABLANCA", "birth_place_ar": "الدار البيضاء", "card_number": "CD987654", "expiry_date": "20.06.2030", "gender": "M"}"""

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


def _is_arabic(text):
    """Check if text contains Arabic characters."""
    for ch in text:
        if "\u0600" <= ch <= "\u06ff" or "\u0750" <= ch <= "\u077f" or "\ufb50" <= ch <= "\ufdff" or "\ufe70" <= ch <= "\ufeff":
            return True
    return False


def _format_detections(detections):
    """Raw text, one per line, original spatial order."""
    return "\n".join(d["text"] for d in detections)


def _parse_json(raw):
    """Extract JSON from LLM response, handling wrapper text."""
    cleaned = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()
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
        "prompt_system": _SYSTEM_PROMPT,
        "prompt_user": f"Extract fields:\n\n{ocr_text}",
    }
