"""
Multi-config PaddleOCR Engine — multiple parameter sets side by side.
"""

import time
import cv2
import numpy as np

# ============================================================
# PaddleOCR configs — each is a different parameter set
# ============================================================

_CONFIGS = {
    "v1_default": {
        "label": "Paddle v1 (default)",
        "params": dict(
            lang='ar',
            text_det_thresh=0.15,
            text_det_box_thresh=0.4,
            text_det_unclip_ratio=1.8,
            text_det_limit_side_len=1920,
            text_det_limit_type='max',
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            text_rec_score_thresh=0.3,
        ),
        "preprocess": None,
    },
    "v2_highres": {
        "label": "Paddle v2 (2560px)",
        "params": dict(
            lang='ar',
            text_det_thresh=0.15,
            text_det_box_thresh=0.3,
            text_det_unclip_ratio=2.0,
            text_det_limit_side_len=2560,
            text_det_limit_type='max',
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            text_rec_score_thresh=0.2,
        ),
        "preprocess": None,
    },
    "v3_upscale": {
        "label": "Paddle v3 (2x upscale + sharpen)",
        "params": dict(
            lang='ar',
            text_det_thresh=0.15,
            text_det_box_thresh=0.4,
            text_det_unclip_ratio=1.8,
            text_det_limit_side_len=2560,
            text_det_limit_type='max',
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            text_rec_score_thresh=0.2,
        ),
        "preprocess": "upscale_sharpen",
    },
}

_loaded = {}


def _preprocess_upscale_sharpen(image):
    """2x upscale + CLAHE + unsharp mask."""
    h, w = image.shape[:2]
    upscaled = cv2.resize(image, (w * 2, h * 2), interpolation=cv2.INTER_CUBIC)
    # CLAHE on L channel
    lab = cv2.cvtColor(upscaled, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    enhanced = cv2.merge([l, a, b])
    enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
    # Unsharp mask
    blur = cv2.GaussianBlur(enhanced, (0, 0), 3)
    sharpened = cv2.addWeighted(enhanced, 1.5, blur, -0.5, 0)
    return sharpened


def _load(key):
    if key in _loaded:
        return _loaded[key]
    from paddleocr import PaddleOCR
    cfg = _CONFIGS[key]
    print(f"  Loading {cfg['label']}...")
    t0 = time.time()
    ocr = PaddleOCR(**cfg["params"])
    print(f"  {cfg['label']} ready ({time.time() - t0:.1f}s)")
    _loaded[key] = ocr
    return ocr


def _run_one(key, image):
    cfg = _CONFIGS[key]
    ocr = _load(key)

    # Apply preprocessing if specified
    img = image
    if cfg["preprocess"] == "upscale_sharpen":
        img = _preprocess_upscale_sharpen(image)

    t0 = time.time()
    results = ocr.predict(img)
    elapsed_ms = (time.time() - t0) * 1000

    detections = []
    if results:
        r = results[0]
        for i, text in enumerate(r.get("rec_texts", [])):
            score = r["rec_scores"][i] if i < len(r.get("rec_scores", [])) else 0.0
            poly = r["rec_polys"][i].tolist() if i < len(r.get("rec_polys", [])) else []
            detections.append({
                "text": text,
                "confidence": round(float(score), 4),
                "polygon": poly,
            })

    return {
        "label": cfg["label"],
        "detections": detections,
        "time_ms": round(elapsed_ms, 1),
    }


# ============================================================
# Public API
# ============================================================

def run_all_ocr(image):
    """Run all OCR configs on the same image."""
    results = {}

    for key in _CONFIGS:
        try:
            results[key] = _run_one(key, image)
            n = len(results[key]["detections"])
            ms = results[key]["time_ms"]
            print(f"    {results[key]['label']}: {n} detections in {ms}ms")
        except Exception as e:
            print(f"    {key}: FAILED — {e}")
            results[key] = {
                "label": _CONFIGS[key]["label"],
                "detections": [],
                "time_ms": 0,
                "error": str(e),
            }

    return results
