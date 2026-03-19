"""
Document type definitions: keywords, schemas, and prompts.
Add or edit document types here — no code changes needed elsewhere.
"""

DOCUMENTS = {
    "cnie_front": {
        "name": "CNIE Front",
        "keywords_fr": ["CARTE NATIONALE", "Né le", "Née le", "Valable jusqu'au"],
        "keywords_ar": ["البطاقة الوطنية", "مزداد بتاريخ", "مزدادة بتاريخ", "صالحة الى غاية"],
        "schema": {
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
        },
        "prompt": """This is the FRONT of a Moroccan CNIE (national ID card).
Think 2-3 lines max, then JSON.
- strip "a " from birth_place_fr
- keep dates as printed (DD.MM.YYYY)
- FR and AR fields refer to the same value. If one looks garbled, produce the correct version. Always output a real word, never garbled OCR.
- null if missing""",
    },
    "cnie_back": {
        "name": "CNIE Back",
        "keywords_fr": ["Adresse", "Etat civil", "Profession"],
        "keywords_ar": ["العنوان", "الحالة المدنية", "المهنة"],
        "schema": {
            "address_fr": "",
            "address_ar": "",
            "city_fr": "",
            "city_ar": "",
            "civil_status_fr": "",
            "civil_status_ar": "",
            "profession_fr": "",
            "profession_ar": "",
        },
        "prompt": """This is the BACK of a Moroccan CNIE (national ID card).
Think 2-3 lines max, then JSON.
- FR and AR fields refer to the same value. If one looks garbled, produce the correct version. Always output a real word, never garbled OCR.
- null if missing""",
    },
    "passport_front": {
        "name": "Passport Info Page",
        "keywords_fr": ["PASSEPORT", "PASSPORT", "Lieu de naissance", "Date de délivrance"],
        "keywords_ar": ["جواز السفر", "جواز سفر", "مكان الازدياد"],
        "schema": {
            "last_name_fr": "",
            "last_name_ar": "",
            "first_name_fr": "",
            "first_name_ar": "",
            "birth_date": "",
            "birth_place_fr": "",
            "nationality_fr": "",
            "nationality_ar": "",
            "passport_number": "",
            "issue_date": "",
            "expiry_date": "",
            "gender": "",
        },
        "prompt": """This is a Moroccan PASSPORT info page.
Think 2-3 lines max, then JSON.
- keep dates as printed (DD.MM.YYYY)
- FR and AR fields refer to the same value. If one looks garbled, produce the correct version. Always output a real word, never garbled OCR.
- null if missing""",
    },
    "passport_back": {
        "name": "Passport MRZ Page",
        "keywords_fr": ["P<MAR", "<<<"],
        "keywords_ar": [],
        "schema": {
            "mrz_line1": "",
            "mrz_line2": "",
        },
        "prompt": """This is a Moroccan PASSPORT MRZ (machine readable zone) page.
Extract the two MRZ lines exactly as printed. JSON only.
- null if missing""",
    },
}

# When classifier is unsure, LLM gets all schemas and decides
FALLBACK_PROMPT = """This is a Moroccan identity document. First identify the type, then extract fields.
Think 2-3 lines max: state the document type, then output the matching JSON.

Possible types:
{types_block}

Pick ONE type. Output its JSON only. null if missing.
FR and AR fields refer to the same value. If one looks garbled, produce the correct version."""
