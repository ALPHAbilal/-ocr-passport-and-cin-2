"""
Multi-model LLM extractor for CNIE OCR pipeline.

Five models run side by side (ID-assignment approach):
1. Phi-3.5-mini (3.8B) — baseline
2. Phi-4-mini (3.8B) — 200K vocab, native Arabic
3. Llama-3.1-8B-Instruct — Meta's 8B instruct model
4. Mistral-7B-Instruct-v0.1 — Mistral's 7B instruct model
5. NuExtract-1.5 — template-based extraction (Phi-3.5 fine-tune)
"""

import json
import os
import re
import time

from huggingface_hub import hf_hub_download
from llama_cpp import Llama, LlamaGrammar

# --- Shared ---
_N_THREADS = os.cpu_count() or 4
_N_CTX = 2048

_FIELDS = [
    "last_name_fr", "last_name_ar", "first_name_fr", "first_name_ar",
    "birth_date", "birth_place_fr", "birth_place_ar",
    "card_number", "expiry_date", "gender",
]

_models = {}


def _is_arabic(text):
    """Check if text contains Arabic characters."""
    return any("\u0600" <= ch <= "\u06ff" for ch in text)


# Known CNIE boilerplate — these are labels, not data values.
_LABEL_FR = [
    "ROYAUME DU MAROC",
    "CARTE NATIONALE",          # catches "CARTE NATIONALE D'IDENTITE" too
    "Né le",
    "Née le",
    "Valable jusqu'au",
]

_LABEL_AR = [
    "المملكة",
    "المعربية",                  # OCR misread of المغربية
    "المغربية",
    "البطاقة الوطنية",
    "للتعريف",
    "صالحة الى غاية",
    "مزداد بتاريخ",
    "مزداد بتانيخ",              # OCR misread of بتاريخ
    "مزدادة بتاريخ",
]


def _is_label(text):
    """Check if text matches a known CNIE label (boilerplate)."""
    t = text.strip()
    for lbl in _LABEL_FR:
        if lbl.lower() in t.lower():
            return True
    for lbl in _LABEL_AR:
        if lbl in t:
            return True
    return False


def _line_tag(text):
    """Return [LABEL], [AR], or [FR] for an OCR line."""
    if _is_label(text):
        return "[LABEL]"
    return "[AR]" if _is_arabic(text) else "[FR]"


# ============================================================
# Shared prompt and grammar (used by all ID-assignment models)
# ============================================================

_PHI_PROMPT = """Vous êtes un extracteur JSON pour carte nationale d'identité marocaine (CNIE).

Tâche : À partir des lignes OCR numérotées, indiquez pour chaque champ UN SEUL numéro de ligne (entier).

Contraintes :
- [LABEL] = étiquette fixe. Ne jamais utiliser comme valeur.
- Les champs _ar DOIVENT pointer vers une ligne [AR].
- Les champs _fr DOIVENT pointer vers une ligne [FR].
- Aucun doublon : chaque numéro de ligne est utilisé AU PLUS UNE FOIS.
- Si le champ est absent ou illisible, mettez null.
- Renvoyez UNIQUEMENT l'objet JSON, sans texte avant ou après.

Comment identifier les noms :
  Les noms apparaissent comme 2 PAIRES consécutives juste après les en-têtes [LABEL].
  Chaque paire = une ligne [AR] suivie d'une ligne [FR] avec le MÊME nom dans les deux écritures.
  Paire 1 (plus haut) = last_name (nom de famille). Paire 2 (juste en dessous) = first_name (prénom).
  IMPORTANT : last_name et first_name sont deux mots DIFFÉRENTS. Si vous trouvez le même mot
  pour les deux, c'est une erreur — cherchez le mot différent sur les lignes adjacentes.
  Indice : une ligne [AR] et la ligne [FR] juste à côté qui contiennent des lettres-only
  (pas de chiffres, pas de dates) forment une paire nom.

Champs : last_name_fr, last_name_ar, first_name_fr, first_name_ar,
         birth_date, birth_place_fr, birth_place_ar, card_number, expiry_date, gender

Exemple d'entrée :
[0] [LABEL] المملكة
[1] [LABEL] ROYAUME DU MAROC
[2] [LABEL] البطاقة الوطنية
[3] [LABEL] CARTE NATIONALE D'IDENTITE
[4] [AR] العلوي
[5] [FR] ALAOUI
[6] [AR] محمد
[7] [FR] MOHAMMED
[8] [LABEL] Né le
[9] [FR] 15.06.1990
[10] [LABEL] مزداد بتاريخ
[11] [AR] الدار البيضاء
[12] [FR] a CASABLANCA
[13] [LABEL] Valable jusqu'au
[14] [FR] 20.06.2030
[15] [LABEL] صالحة الى غاية
[16] [FR] AB123456
[17] [FR] M

Exemple de sortie :
{"last_name_fr": 5, "last_name_ar": 4, "first_name_fr": 7, "first_name_ar": 6, "birth_date": 9, "birth_place_fr": 12, "birth_place_ar": 11, "card_number": 16, "expiry_date": 14, "gender": 17}
"""

# GBNF grammar: forces output to be exactly our JSON schema with integers/null
_GRAMMAR_STR = r"""
root ::= "{" ws kv0 "," ws kv1 "," ws kv2 "," ws kv3 "," ws kv4 "," ws kv5 "," ws kv6 "," ws kv7 "," ws kv8 "," ws kv9 ws "}"
kv0 ::= "\"last_name_fr\"" ws ":" ws val
kv1 ::= "\"last_name_ar\"" ws ":" ws val
kv2 ::= "\"first_name_fr\"" ws ":" ws val
kv3 ::= "\"first_name_ar\"" ws ":" ws val
kv4 ::= "\"birth_date\"" ws ":" ws val
kv5 ::= "\"birth_place_fr\"" ws ":" ws val
kv6 ::= "\"birth_place_ar\"" ws ":" ws val
kv7 ::= "\"card_number\"" ws ":" ws val
kv8 ::= "\"expiry_date\"" ws ":" ws val
kv9 ::= "\"gender\"" ws ":" ws val
val ::= integer | "null"
integer ::= "0" | [1-9] [0-9]*
ws ::= [ \t\n]*
"""

# ============================================================
# Model configs
# ============================================================

_MODEL_CONFIGS = [
    # {
    #     "key": "phi35",
    #     "name": "Phi-3.5-mini",
    #     "label": "Phi-3.5-mini (ID-assign)",
    #     "repo": "bartowski/Phi-3.5-mini-instruct-GGUF",
    #     "file": "Phi-3.5-mini-instruct-Q4_K_M.gguf",
    #     "type": "id_assign",
    # },
    # {
    #     "key": "phi4",
    #     "name": "Phi-4-mini",
    #     "label": "Phi-4-mini (ID-assign)",
    #     "repo": "unsloth/Phi-4-mini-instruct-GGUF",
    #     "file": "Phi-4-mini-instruct-Q4_K_M.gguf",
    #     "type": "id_assign",
    # },
    # {
    #     "key": "llama31",
    #     "name": "Llama-3.1-8B",
    #     "label": "Llama-3.1-8B (ID-assign)",
    #     "repo": "bartowski/Meta-Llama-3.1-8B-Instruct-GGUF",
    #     "file": "Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf",
    #     "type": "id_assign",
    # },
    # {
    #     "key": "mistral7b",
    #     "name": "Mistral-7B-v0.1",
    #     "label": "Mistral-7B (ID-assign)",
    #     "repo": "TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
    #     "file": "mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    #     "type": "id_assign",
    # },
    # {
    #     "key": "nuextract",
    #     "name": "NuExtract-1.5",
    #     "label": "NuExtract-1.5",
    #     "repo": "bartowski/NuExtract-v1.5-GGUF",
    #     "file": "NuExtract-v1.5-Q4_K_M.gguf",
    #     "type": "nuextract",
    # },
    # {
    #     "key": "gemma2",
    #     "name": "Gemma-2-9B",
    #     "label": "Gemma-2-9B (ID-assign)",
    #     "repo": "bartowski/gemma-2-9b-it-GGUF",
    #     "file": "gemma-2-9b-it-Q4_K_M.gguf",
    #     "type": "id_assign",
    # },
    # {
    #     "key": "qwen25",
    #     "name": "Qwen2.5-7B",
    #     "label": "Qwen2.5-7B (ID-assign)",
    #     "repo": "bartowski/Qwen2.5-7B-Instruct-GGUF",
    #     "file": "Qwen2.5-7B-Instruct-Q4_K_M.gguf",
    #     "type": "id_assign",
    # },
    {
        "key": "nemo",
        "name": "Mistral-Nemo-12B",
        "label": "Mistral-Nemo-12B (ID-assign)",
        "repo": "bartowski/Mistral-Nemo-Instruct-2407-GGUF",
        "file": "Mistral-Nemo-Instruct-2407-Q4_K_M.gguf",
        "type": "id_assign",
    },
]

_NUEXTRACT_TEMPLATE = json.dumps({
    "last_name_fr": "",
    "last_name_ar": "",
    "first_name_fr": "",
    "first_name_ar": "",
    "birth_date": "",
    "birth_place_fr": "",
    "birth_place_ar": "",
    "card_number": "",
    "expiry_date": "",
    "gender": "",
}, ensure_ascii=False)


# ============================================================
# Sequential model loading — one at a time to save memory
# ============================================================

# Pre-download all GGUF files at startup (fast if cached)
_model_paths = {}

print("Pre-downloading GGUF files...")
for cfg in _MODEL_CONFIGS:
    try:
        path = hf_hub_download(repo_id=cfg["repo"], filename=cfg["file"])
        _model_paths[cfg["key"]] = path
        print(f"  {cfg['name']}: ready")
    except Exception as e:
        print(f"  WARNING: {cfg['name']} download failed: {e}")

# Parse grammar once (used by all ID-assignment models)
_phi_grammar = None
try:
    _phi_grammar = LlamaGrammar.from_string(_GRAMMAR_STR)
except Exception as e:
    print(f"  WARNING: GBNF grammar failed: {e}")

print(f"Models available: {list(_model_paths.keys())}")


def _load_model(key):
    """Load a single model into memory. Returns Llama instance or None."""
    if key not in _model_paths:
        return None
    cfg = next(c for c in _MODEL_CONFIGS if c["key"] == key)
    try:
        print(f"  Loading {cfg['name']} ({_N_THREADS} threads)...")
        t0 = time.time()
        llm = Llama(model_path=_model_paths[key], n_ctx=_N_CTX, n_threads=_N_THREADS, verbose=False)
        print(f"  {cfg['name']} ready ({time.time() - t0:.1f}s)")
        return llm
    except Exception as e:
        print(f"  WARNING: {cfg['name']} failed to load: {e}")
        return None


def _unload_model(llm):
    """Free model memory."""
    del llm
    import gc
    gc.collect()


# ============================================================
# Shared helpers
# ============================================================

def _parse_json(raw):
    """Extract JSON from LLM response."""
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


def _clean_place_fr(val):
    """Strip 'a ' prefix, uppercase."""
    if not val:
        return None
    val = val.strip()
    if val.lower().startswith("a "):
        val = val[2:]
    return val.strip().upper() or None


def _clean_place_ar(val):
    """Strip 'ب ' prefix."""
    if not val:
        return None
    val = val.strip()
    if val.startswith("ب "):
        val = val[2:]
    return val.strip() or None


def _clean_date(val):
    """Extract DD.MM.YYYY, normalize / to ."""
    if not val:
        return None
    m = re.search(r"(\d{2})[./](\d{2})[./](\d{4})", val)
    return f"{m.group(1)}.{m.group(2)}.{m.group(3)}" if m else None


def _clean_fields(fields):
    """Post-processing: normalize text from OCR."""
    fields["birth_place_fr"] = _clean_place_fr(fields.get("birth_place_fr"))
    fields["birth_place_ar"] = _clean_place_ar(fields.get("birth_place_ar"))
    fields["birth_date"] = _clean_date(fields.get("birth_date"))
    fields["expiry_date"] = _clean_date(fields.get("expiry_date"))

    cn = (fields.get("card_number") or "").strip().upper()
    fields["card_number"] = cn or None

    g = (fields.get("gender") or "").strip().upper()
    fields["gender"] = g if g in ("M", "F") else None

    for key in ("last_name_fr", "first_name_fr"):
        val = (fields.get(key) or "").strip().upper()
        fields[key] = val or None

    for key in ("last_name_ar", "first_name_ar"):
        val = (fields.get(key) or "").strip()
        fields[key] = val or None

    return fields


def _fix_name_order(fields, detections, id_map):
    """
    Use Y-coordinates to validate name ordering.
    On CNIE: family name (النسب) is ABOVE given name (الاسم).
    """
    last_id = id_map.get("last_name_fr")
    first_id = id_map.get("first_name_fr")

    if not isinstance(last_id, (int, float)) or not isinstance(first_id, (int, float)):
        return fields

    last_idx = int(last_id)
    first_idx = int(first_id)

    if not (0 <= last_idx < len(detections) and 0 <= first_idx < len(detections)):
        return fields

    last_poly = detections[last_idx].get("polygon", [])
    first_poly = detections[first_idx].get("polygon", [])

    if not last_poly or not first_poly:
        return fields

    last_y = sum(p[1] for p in last_poly) / len(last_poly)
    first_y = sum(p[1] for p in first_poly) / len(first_poly)

    # Family name should be higher on card (smaller Y)
    if last_y > first_y:
        fields["last_name_fr"], fields["first_name_fr"] = fields["first_name_fr"], fields["last_name_fr"]
        fields["last_name_ar"], fields["first_name_ar"] = fields["first_name_ar"], fields["last_name_ar"]

    return fields


# ============================================================
# Generic ID-assignment extraction (used by all instruct models)
# ============================================================

def _extract_id_assign(llm, label, detections):
    """ID-assignment: number lines, get IDs back, resolve to text."""
    lines = []
    for i, d in enumerate(detections):
        tag = _line_tag(d["text"])
        lines.append(f"[{i}] {tag} {d['text']}")
    numbered = "\n".join(lines)
    user_msg = f"Lignes OCR:\n\n{numbered}"

    t0 = time.time()
    kwargs = dict(
        messages=[
            {"role": "system", "content": _PHI_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        max_tokens=256,
        temperature=0.1,
    )
    if _phi_grammar:
        kwargs["grammar"] = _phi_grammar
    else:
        kwargs["response_format"] = {"type": "json_object"}

    response = llm.create_chat_completion(**kwargs)
    elapsed_ms = (time.time() - t0) * 1000

    raw = response["choices"][0]["message"]["content"]
    id_map = _parse_json(raw)

    if id_map is None:
        return {
            "label": label,
            "fields": None,
            "time_ms": round(elapsed_ms, 1),
            "raw": raw,
            "prompt_system": _PHI_PROMPT,
            "prompt_user": user_msg,
        }

    # Resolve IDs → OCR text
    fields = {}
    for field in _FIELDS:
        line_id = id_map.get(field)
        if line_id is None or not isinstance(line_id, (int, float)):
            fields[field] = None
            continue
        idx = int(line_id)
        fields[field] = detections[idx]["text"] if 0 <= idx < len(detections) else None

    fields = _clean_fields(fields)

    return {
        "label": label,
        "fields": fields,
        "time_ms": round(elapsed_ms, 1),
        "raw": raw,
        "prompt_system": _PHI_PROMPT,
        "prompt_user": user_msg,
    }


# ============================================================
# NuExtract-1.5 extraction (template-based)
# ============================================================

def _extract_nuextract(llm, detections):
    """Template extraction: NuExtract fills in JSON from OCR text."""
    # Plain text, one per line (NuExtract copies from this)
    ocr_text = "\n".join(d["text"] for d in detections)

    prompt = f"<|input|>\n### Template:\n{_NUEXTRACT_TEMPLATE}\n### Text:\n{ocr_text}\n<|output|>\n"

    t0 = time.time()
    response = llm(
        prompt,
        max_tokens=512,
        temperature=0.0,
        stop=["<|input|>", "<|end|>", "<|endoftext|>"],
    )
    elapsed_ms = (time.time() - t0) * 1000

    raw = response["choices"][0]["text"]
    fields = _parse_json(raw)

    if fields:
        # Ensure all expected fields exist
        for f in _FIELDS:
            if f not in fields:
                fields[f] = None
            elif fields[f] == "":
                fields[f] = None
        fields = _clean_fields(fields)

    return {
        "label": "NuExtract-1.5",
        "fields": fields,
        "time_ms": round(elapsed_ms, 1),
        "raw": raw,
        "prompt_system": None,
        "prompt_user": prompt,
    }


# ============================================================
# Public API
# ============================================================

def extract_fields_all(detections):
    """
    Run all available models sequentially on the same OCR detections.
    Loads one model at a time to save memory.
    Returns dict of model_key → result.
    """
    results = {}

    for cfg in _MODEL_CONFIGS:
        key = cfg["key"]
        if key not in _model_paths:
            continue

        print(f"\n>> Running {cfg['name']}...")
        llm = _load_model(key)
        if llm is None:
            continue

        try:
            if cfg["type"] == "id_assign":
                results[key] = _extract_id_assign(llm, cfg["label"], detections)
            elif cfg["type"] == "nuextract":
                results[key] = _extract_nuextract(llm, detections)
        except Exception as e:
            print(f"  ERROR: {cfg['name']} extraction failed: {e}")
            results[key] = {
                "label": cfg["label"],
                "fields": None,
                "time_ms": 0,
                "raw": str(e),
                "prompt_system": None,
                "prompt_user": None,
            }
        finally:
            _unload_model(llm)

    return results


def get_loaded_models():
    """Return list of available model keys (downloaded, not necessarily in memory)."""
    return list(_model_paths.keys())
