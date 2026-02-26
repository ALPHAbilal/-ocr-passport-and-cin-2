# Flask OCR Extraction Endpoint — Implementation Plan

## Context

We've spent days getting PaddleOCR v3.4 + PP-OCRv5 working with the correct dependency chain (Python 3.11, paddlepaddle 3.2.1, paddleocr 3.4.0). The notebook (`paddleocr_test.ipynb`) has proven working patterns. Now we need to package this into a Flask API endpoint.

**Key constraint:** Preserve the exact API patterns that work — no guessing, no deprecated params. Every line of OCR code comes from the tested notebook.

---

## What Already Exists

| File | What it does |
|------|-------------|
| `services/preprocessor.py` (218 lines) | Card detection + perspective correction + resize to 856x540. Functions: `preprocess_card(image_bytes)`, `find_card_contour()`, `four_point_warp()`, `ensure_landscape()` |
| `calibration-tool/test_server.py` (62 lines) | Existing Flask server with `/preprocess` endpoint — good pattern reference |
| `paddleocr_test.ipynb` | All tested OCR patterns: init, `.predict()`, result parsing, preprocessing |

---

## What We Build

### Files to Create

**1. `services/ocr_engine.py`** — PaddleOCR wrapper (singleton)

```python
# Exact init pattern from notebook cell 5 — DO NOT CHANGE PARAMS
ocr_ar = PaddleOCR(lang='ar', text_rec_score_thresh=0.3)  # Arabic
ocr_fr = PaddleOCR(lang='fr', text_rec_score_thresh=0.3)  # French + English (Latin)
```

- Two models only: `ar` and `fr` (no separate English — French model reads Latin scripts)
- Models loaded ONCE at module import (singleton pattern)
- One function: `run_ocr(image_path, lang)` → returns list of `{text, confidence, polygon}`
- Uses `.predict()` API (v3.4) — NOT `.ocr()` (deprecated)
- Result parsing: `results[0].get("rec_texts")`, `results[0].get("rec_scores")`, `results[0].get("rec_polys")`
- Saves image to temp file for `.predict()` (it works best with file paths, tested in notebook)

**2. `app.py`** — Flask endpoint

- `POST /extract` — accepts image file upload
- Params: `preprocess` = `raw` | `upscale_2x` (default: `raw`)
- Flow:
  1. Read uploaded image bytes
  2. Run `preprocess_card(image_bytes)` from existing `services/preprocessor.py` (card detection + perspective warp + 856x540)
  3. Apply preprocessing: raw (no-op) or upscale_2x (cv2.resize 2x with INTER_CUBIC)
  4. Save to temp file
  5. Run both `ar` and `fr` models on full image
  6. Return raw results as JSON
- No field cropping, no coordinate mapping — raw OCR output

**3. `requirements.txt`** — Pinned versions

```
flask>=3.0.0
opencv-python>=4.8.0
numpy>=1.24.0
paddlepaddle==3.2.1
paddleocr==3.4.0
Pillow>=10.0.0
```

### Files to Modify

**None.** `services/preprocessor.py` stays as-is. It already does exactly what we need (card detection + perspective correction).

---

## Endpoint Spec

### `POST /extract`

**Request:**
- Content-Type: `multipart/form-data`
- `image`: file upload (JPEG/PNG)
- `preprocess`: form field, optional — `raw` (default) or `upscale_2x`

**Response (200):**
```json
{
  "success": true,
  "preprocessing": "raw",
  "card_detection": {
    "method": "card_found",
    "original_size": "1920x1080",
    "warped_size": "864x540"
  },
  "results": {
    "arabic": {
      "regions_found": 5,
      "time_ms": 320,
      "detections": [
        {"text": "سفيان", "confidence": 0.85, "polygon": [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]},
        "..."
      ]
    },
    "french": {
      "regions_found": 8,
      "time_ms": 280,
      "detections": [
        {"text": "SOUFIANE", "confidence": 0.92, "polygon": [[x1,y1], "..."]},
        "..."
      ]
    }
  },
  "total_time_ms": 650
}
```

**Error (400/422):**
```json
{
  "success": false,
  "error": "No image file provided"
}
```

---

## Architecture

```
POST /extract (image file + preprocess param)
    │
    ▼
services/preprocessor.py  ← EXISTS, NO CHANGES
    preprocess_card(image_bytes)
    → card detection (Canny + adaptive threshold)
    → perspective warp (4-point transform)
    → landscape orientation fix
    → resize to 856x540
    │
    ▼
Preprocessing layer (in app.py, simple)
    raw: no-op
    upscale_2x: cv2.resize(img, fx=2, fy=2, INTER_CUBIC)
    │
    ▼
services/ocr_engine.py  ← NEW
    run_ocr(image_path, 'ar') → raw detections
    run_ocr(image_path, 'fr') → raw detections
    │
    ▼
JSON response with raw results from both models
```

---

## Critical References — What Works (from notebook)

### PaddleOCR Init (notebook cell 5)
```python
# THESE EXACT PARAMS — nothing else
ocr_ar = PaddleOCR(lang='ar', text_rec_score_thresh=0.3)
ocr_fr = PaddleOCR(lang='fr', text_rec_score_thresh=0.3)
```

**DO NOT USE (deprecated/broken in v3.4):** `use_angle_cls`, `use_gpu`, `ocr_version`, `drop_score`, `show_log`, `det=False`

### Prediction + Result Parsing (notebook cells 7, 14)
```python
results = ocr.predict(image_path)  # file path, not numpy array
if results:
    r = results[0]
    rec_texts = r.get("rec_texts", [])
    rec_scores = r.get("rec_scores", [])
    rec_polys = r.get("rec_polys", [])
```

### Preprocessing — upscale_2x (notebook cell 11)
```python
def upscale_2x(img):
    return cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
```

### Card Detection (services/preprocessor.py — already exists)
```python
from services.preprocessor import preprocess_card
result = preprocess_card(image_bytes)
# result["success"] → bool
# result["image"]   → numpy array (856x540 BGR)
# result["debug"]   → {"detection": "card_found", "corners": [...], ...}
```

---

## Dependency Compatibility (TESTED & WORKING)

| Package | Version | Notes |
|---------|---------|-------|
| Python | 3.11 | 3.13 NOT supported by PaddleOCR |
| paddlepaddle | 3.2.1 | CPU version |
| paddleocr | 3.4.0 | PP-OCRv5 auto-selected (supports Arabic) |
| flask | >=3.0.0 | |
| opencv-python | >=4.8.0 | |
| numpy | >=1.24.0 | |

PP-OCRv5 supports Arabic + all Latin languages. It is auto-selected by default in PaddleOCR v3.4 (no need to specify `ocr_version`). Note: PP-OCRv4 only supported Chinese and English — we skip it entirely.

---

## Verification Steps

1. Start the server: `python app.py`
2. Test with curl:
   ```bash
   curl -X POST -F "image=@front.jpeg" -F "preprocess=raw" http://localhost:5000/extract
   ```
3. Verify response has both `arabic` and `french` results with detected text
4. Test with `preprocess=upscale_2x` and compare
5. Test with an image that has no card (should still work — preprocessor falls back to full image resize)
6. Test with invalid input (no image) — should return 400 error
