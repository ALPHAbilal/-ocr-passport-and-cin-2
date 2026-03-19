"""
LLM field extractor for CNIE/Passport OCR pipeline.
GPT-OSS-20B via llama-cpp-python.
Classifies document type by keywords, loads matching prompt.
"""

import gc
import json
import re
import os
import time

from huggingface_hub import hf_hub_download
from llama_cpp import Llama

from services.document_config import DOCUMENTS, FALLBACK_PROMPT

_N_THREADS = os.cpu_count() or 4
_N_CTX = 2048
_MODEL_REPO = "bartowski/openai_gpt-oss-20b-GGUF"
_MODEL_FILE = "openai_gpt-oss-20b-Q4_K_M.gguf"
_CONFIDENCE_THRESHOLD = 0.95

# Download model at startup
_model_path = None

print("Downloading GPT-OSS-20B...")
try:
    _model_path = hf_hub_download(repo_id=_MODEL_REPO, filename=_MODEL_FILE)
    print("  GPT-OSS-20B: ready")
except Exception as e:
    print(f"  WARNING: download failed: {e}")


# --- Classifier ---

def _classify(ocr_text):
    """Score each document type by keyword matches. Returns (doc_key, confidence)."""
    text_lower = ocr_text.lower()
    scores = {}

    for key, doc in DOCUMENTS.items():
        hits = 0
        total = len(doc["keywords_fr"]) + len(doc["keywords_ar"])
        if total == 0:
            continue
        for kw in doc["keywords_fr"]:
            if kw.lower() in text_lower:
                hits += 1
        for kw in doc["keywords_ar"]:
            if kw in ocr_text:
                hits += 1
        scores[key] = hits / total

    if not scores:
        return None, 0.0

    best = max(scores, key=scores.get)
    return best, scores[best]


# --- Prompt builders ---

def _build_focused_prompt(doc_key):
    """High confidence: one schema, one prompt."""
    doc = DOCUMENTS[doc_key]
    schema = json.dumps(doc["schema"], ensure_ascii=False)
    return f"{doc['prompt']}\n{schema}"


def _build_fallback_prompt():
    """Low confidence: all schemas, LLM decides."""
    types_block = ""
    for key, doc in DOCUMENTS.items():
        schema = json.dumps(doc["schema"], ensure_ascii=False)
        types_block += f'- {doc["name"]}: {schema}\n'
    return FALLBACK_PROMPT.replace("{types_block}", types_block.strip())


# --- JSON extraction ---

def _extract_json(text):
    """Find the last JSON object in text (after reasoning)."""
    matches = list(re.finditer(r'\{[^{}]*\}', text, re.DOTALL))
    for m in reversed(matches):
        try:
            return json.loads(m.group())
        except json.JSONDecodeError:
            continue
    return None


# --- Main ---

def extract_fields_all(detections):
    if not _model_path:
        return {}

    ocr_text = "\n".join(d["text"] for d in detections)

    # Classify
    doc_key, confidence = _classify(ocr_text)

    if confidence >= _CONFIDENCE_THRESHOLD and doc_key:
        system_prompt = _build_focused_prompt(doc_key)
        doc_name = DOCUMENTS[doc_key]["name"]
    else:
        system_prompt = _build_fallback_prompt()
        doc_name = f"Unknown ({confidence:.0%})"

    # Load → run → unload
    llm = Llama(model_path=_model_path, n_ctx=_N_CTX, n_threads=_N_THREADS, verbose=False)

    t0 = time.time()
    response = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
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
            "label": f"GPT-OSS-20B — {doc_name}",
            "fields": fields,
            "time_ms": round(elapsed_ms, 1),
            "raw": raw,
            "prompt_system": system_prompt,
            "prompt_user": ocr_text,
        }
    }


def get_loaded_models():
    return ["gpt_oss"] if _model_path else []
