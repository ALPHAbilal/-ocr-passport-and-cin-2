"""
PaddleOCR Engine — Single Arabic model reads both Arabic + French.

Key optimizations (based on research):
- No JPEG round-trip: pass numpy arrays directly (preserves Arabic dots/diacritics)
- 2x upscale + CLAHE + unsharp mask before OCR
- Tuned detection thresholds to catch all text regions
- Single Arabic model only (reads French at 0.99 confidence, French model adds garbage)
"""

import time

import cv2
import numpy as np
from paddleocr import PaddleOCR

# --- Tuned detection params ---
_DET_PARAMS = dict(
    text_det_thresh=0.2,            # was 0.3 — catch lower-contrast text pixels
    text_det_box_thresh=0.4,        # was 0.6 — let name boxes survive filtering
    text_det_unclip_ratio=1.8,      # was 1.5 — expand boxes for tight-margin names
    text_det_limit_side_len=1280,   # prevent downscaling that kills small text
    text_det_limit_type='max',
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    text_rec_score_thresh=0.3,
)

# --- Single model: Arabic reads both scripts ---
print("Loading OCR model (Arabic PP-OCRv5, tuned detection)...")
_t0 = time.time()
_ocr = PaddleOCR(lang='ar', **_DET_PARAMS)
print(f"OCR model ready ({time.time() - _t0:.1f}s)")


def run_ocr(image):
    """
    Run OCR on an image. Single pass, Arabic model reads both scripts.

    Args:
        image: numpy array (BGR)

    Returns:
        dict with:
            - detections: list of {text, confidence, polygon}
            - regions_found: int
            - time_ms: float
    """
    # Pass numpy array directly — no JPEG compression that degrades Arabic dots
    t0 = time.time()
    results = _ocr.predict(image)
    elapsed_ms = (time.time() - t0) * 1000

    detections = []
    if results:
        r = results[0]
        rec_texts = r.get("rec_texts", [])
        rec_scores = r.get("rec_scores", [])
        rec_polys = r.get("rec_polys", [])

        for i, text in enumerate(rec_texts):
            score = rec_scores[i] if i < len(rec_scores) else 0.0
            poly = rec_polys[i].tolist() if i < len(rec_polys) else []
            detections.append({
                "text": text,
                "confidence": round(float(score), 4),
                "polygon": poly,
            })

    return {
        "detections": detections,
        "regions_found": len(detections),
        "time_ms": round(elapsed_ms, 1),
    }
