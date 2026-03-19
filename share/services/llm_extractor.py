"""
LLM field extractor for CNIE OCR pipeline.
GPT-OSS-20B via llama-cpp-python.
Model reasons freely, we extract the JSON from its output.
"""

import gc
import json
import re
import os
import time

from huggingface_hub import hf_hub_download
from llama_cpp import Llama

_N_THREADS = os.cpu_count() or 4
_N_CTX = 2048
_MODEL_REPO = "bartowski/openai_gpt-oss-20b-GGUF"
_MODEL_FILE = "openai_gpt-oss-20b-Q4_K_M.gguf"

_PROMPT = """Extract fields from Moroccan CNIE card OCR. Think 2-3 lines max, then JSON.
{"last_name_fr":"","last_name_ar":"","first_name_fr":"","first_name_ar":"","birth_date":"","birth_place_fr":"","birth_place_ar":"","card_number":"","expiry_date":"","gender":""}
- strip "a " from birth_place_fr
- keep dates as printed (DD.MM.YYYY)
- FR and AR fields refer to the same value. If one looks garbled, produce the correct version from your knowledge of the other. Always output a real word, never garbled OCR.
- null if missing"""

# Download model at startup
_model_path = None

print("Downloading GPT-OSS-20B...")
try:
    _model_path = hf_hub_download(repo_id=_MODEL_REPO, filename=_MODEL_FILE)
    print("  GPT-OSS-20B: ready")
except Exception as e:
    print(f"  WARNING: download failed: {e}")


def _extract_json(text):
    """Find the last JSON object in the text (after any reasoning)."""
    # Find all JSON-like blocks
    matches = list(re.finditer(r'\{[^{}]*\}', text, re.DOTALL))
    # Try from last match backwards (JSON is at the end after reasoning)
    for m in reversed(matches):
        try:
            return json.loads(m.group())
        except json.JSONDecodeError:
            continue
    return None


def extract_fields_all(detections):
    if not _model_path:
        return {}

    ocr_text = "\n".join(d["text"] for d in detections)

    llm = Llama(model_path=_model_path, n_ctx=_N_CTX, n_threads=_N_THREADS, verbose=False)

    t0 = time.time()
    response = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": _PROMPT},
            {"role": "user", "content": ocr_text},
        ],
        max_tokens=1024,
        temperature=0.0,
    )
    elapsed_ms = (time.time() - t0) * 1000
    raw = response["choices"][0]["message"]["content"]

    del llm
    gc.collect()

    parsed = _extract_json(raw)
    fields = None
    if parsed:
        fields = {k: (v if v else None) for k, v in parsed.items()}

    return {
        "gpt_oss": {
            "label": "GPT-OSS-20B",
            "fields": fields,
            "time_ms": round(elapsed_ms, 1),
            "raw": raw,
            "prompt_system": _PROMPT,
            "prompt_user": ocr_text,
        }
    }


def get_loaded_models():
    return ["gpt_oss"] if _model_path else []
