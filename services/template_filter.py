"""
Template text filter — minimal filtering.
Only removes the signer name (which confused the LLM) and low-confidence noise.
The LLM prompt already handles ignoring other template text.
"""

_CONTAINS = [
    "حموشي",
    "المدير العام",
]

MIN_CONFIDENCE = 0.4


def filter_detections(detections):
    kept = []
    for d in detections:
        text = d["text"].strip()

        if d["confidence"] < MIN_CONFIDENCE:
            continue

        if any(sub in text for sub in _CONTAINS):
            continue

        kept.append(d)

    return kept
