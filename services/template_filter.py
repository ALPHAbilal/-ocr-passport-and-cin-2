"""
Template text filter — removes CNIE boilerplate from OCR detections.
Strips headers, labels, signer name, and low-confidence noise.
"""

# Exact matches (normalized: stripped, lowered)
_EXACT = {
    "royaume du maroc",
    "carte nationale d identite",
    "carte nationale d'identite",
    "né le",
    "ne le",
    "valable jusqu au",
    "valable jusqu'au",
    "m",  # single M often appears as gender AND as template — keep only if needed
    "f",
    "المملكة",
    "المغربية",
    "المعربية",
    "البطاقة الوطنية",
    "للتعريف",
    "مزداد بتاريخ",
    "مزداد بتانيخ",
    "صالحة الى غاية",
    "المدير العام للأمن الوطني",
    "المدير العام للإمن الوطنى",
    "عبد اللطيف حموشي",
    "عبد اللطيّف حموشي",
}

# Substrings — if any of these appear inside a detection, skip it
_CONTAINS = [
    "المدير العام",
    "حموشي",
]

MIN_CONFIDENCE = 0.5


def filter_detections(detections):
    """
    Filter out template/boilerplate text and low-confidence noise.

    Args:
        detections: list of {"text": str, "confidence": float}

    Returns:
        list of detections with boilerplate removed
    """
    kept = []
    for d in detections:
        text = d["text"].strip()
        conf = d["confidence"]

        if conf < MIN_CONFIDENCE:
            continue

        normalized = text.lower().strip()
        if normalized in _EXACT:
            continue

        if any(sub in text for sub in _CONTAINS):
            continue

        kept.append(d)

    return kept
