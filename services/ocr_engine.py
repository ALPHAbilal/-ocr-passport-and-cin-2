"""
PaddleOCR Engine — Singleton wrapper for Arabic + French OCR.

Models loaded ONCE at module import. Uses PaddleOCR v3.4 .predict() API.
DO NOT use .ocr() (deprecated) or params like use_angle_cls, use_gpu, ocr_version, drop_score, show_log.
"""

import os
import tempfile
import time

import cv2
import numpy as np
from paddleocr import PaddleOCR

# --- Singleton model instances (loaded once at import) ---
print("Loading Arabic OCR model (PP-OCRv5)...")
_t0 = time.time()
ocr_ar = PaddleOCR(lang='ar', text_rec_score_thresh=0.3)
print(f"Arabic model ready ({time.time() - _t0:.1f}s)")

print("Loading French OCR model (PP-OCRv5)...")
_t0 = time.time()
ocr_fr = PaddleOCR(lang='fr', text_rec_score_thresh=0.3)
print(f"French model ready ({time.time() - _t0:.1f}s)")

_OCR_INSTANCES = {
    "ar": ocr_ar,
    "fr": ocr_fr,
}


def run_ocr(image, lang):
    """
    Run PaddleOCR on an image.

    Args:
        image: numpy array (BGR) or file path string
        lang: 'ar' or 'fr'

    Returns:
        dict with:
            - detections: list of {text, confidence, polygon}
            - regions_found: int
            - time_ms: float
    """
    if lang not in _OCR_INSTANCES:
        raise ValueError(f"Unsupported lang '{lang}'. Use 'ar' or 'fr'.")

    ocr = _OCR_INSTANCES[lang]

    # .predict() works best with file paths (tested in notebook)
    tmp_path = None
    if isinstance(image, np.ndarray):
        fd, tmp_path = tempfile.mkstemp(suffix=".jpg")
        os.close(fd)
        cv2.imwrite(tmp_path, image)
        predict_input = tmp_path
    else:
        predict_input = image

    try:
        t0 = time.time()
        results = ocr.predict(predict_input)
        elapsed_ms = (time.time() - t0) * 1000
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

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
