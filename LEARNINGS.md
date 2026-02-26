# CNIE OCR Pipeline — Learnings & Compatibility Reference

Everything we learned building this pipeline. Read this before changing anything.

---

## 1. Final Working Stack

| Package | Version | Why this exact version |
|---------|---------|----------------------|
| Python | **3.11** | 3.13 breaks PaddleOCR + PyTorch. 3.10 also works. |
| paddlepaddle | **3.2.1** | CPU version. Tested working with paddleocr 3.4.0. |
| paddleocr | **3.4.0** | Uses PP-OCRv5 by default. Supports Arabic. New `.predict()` API. |
| flask | >=3.0.0 | Standard |
| opencv-python | >=4.8.0 | Standard |
| numpy | >=1.24.0 | Standard |
| Pillow | >=10.0.0 | Image I/O support |

**Virtual environment:** `venv311` created with `py -3.11 -m venv venv311`

---

## 2. PaddleOCR v3.4 API — What Works

### Initialization (EXACT params that work)
```python
from paddleocr import PaddleOCR

ocr_ar = PaddleOCR(lang='ar', text_rec_score_thresh=0.3)
ocr_fr = PaddleOCR(lang='fr', text_rec_score_thresh=0.3)
```

PP-OCRv5 is auto-selected. No need to specify `ocr_version`.

### Prediction
```python
results = ocr.predict(image_path)   # file path string — NOT numpy array
```

### Result Parsing
```python
if results:
    r = results[0]
    rec_texts = r.get("rec_texts", [])    # list of strings
    rec_scores = r.get("rec_scores", [])  # list of floats
    rec_polys = r.get("rec_polys", [])    # list of polygon coords
```

### DEPRECATED — DO NOT USE
These params are from PaddleOCR v2.x / v3.3 and **crash or are ignored** in v3.4:

| Param | Status |
|-------|--------|
| `use_angle_cls` | Removed |
| `use_gpu` | Removed |
| `ocr_version` | Removed (auto-selects PP-OCRv5) |
| `drop_score` | Renamed to `text_rec_score_thresh` |
| `show_log` | Removed |
| `det=False` | Not a param in `.predict()` |
| `.ocr()` method | Deprecated — use `.predict()` |

---

## 3. Errors We Hit & How We Fixed Them

### Surya OCR — `pad_token_id` AttributeError
- **Error:** `'SuryaDecoderConfig' object has no attribute 'pad_token_id'`
- **Cause:** surya-ocr 0.17.1 requires `transformers >= 4.56.1`. HuggingFace version numbering jumped from 4.39.x directly to 4.56.0 (not sequential).
- **We had:** transformers 5.2.0 (too new) then tried 4.46.3 (doesn't exist in the way we expected)
- **Fix:** `pip install transformers==4.56.1`
- **Outcome:** Surya loaded but OCR results were poor. Abandoned it.

### PaddleOCR — Arabic not supported in PP-OCRv4
- **Error:** `ValueError: No models are available for the language 'ar' and OCR version 'PP-OCRv4'`
- **Cause:** PP-OCRv4 only supports Chinese (`ch`) and English (`en`). Arabic requires PP-OCRv5.
- **Fix:** Don't specify `ocr_version` — let it default to PP-OCRv5.

### PaddleOCR — torch DLL loading failure
- **Error:** `OSError: [WinError 127] Error loading "...\torch\lib\shm.dll"`
- **Cause:** PaddleOCR v3.x pulls in paddlex → modelscope → torch as transitive dependency
- **Fix:** Uninstall everything, reinstall paddlepaddle 3.2.1 and paddleocr 3.4.0 cleanly

### Jupyter using wrong Python
- **Problem:** `pip install` in terminal went to system Python 3.13, but notebook used a different interpreter
- **Fix:** Use `import sys; !{sys.executable} -m pip install ...` inside notebook cells
- **Permanent fix:** Created venv311 with Python 3.11, registered as Jupyter kernel

### Python 3.13 — breaks everything
- **Problem:** Both surya-ocr and PaddleOCR don't support Python 3.13. PyTorch wheels also missing for 3.13.
- **Fix:** Use Python 3.11 (or 3.10)

### Missing matplotlib in venv
- **Error:** `ModuleNotFoundError: No module named 'matplotlib'`
- **Fix:** `pip install matplotlib` in the venv311 environment

---

## 4. OCR Engines Tested — Results

### PaddleOCR PP-OCRv5 (WINNER)
- Arabic: Works well with `lang='ar'`
- French/English: Works well with `lang='fr'` (handles all Latin scripts)
- Speed: ~200-400ms per full image on CPU
- Confidence scores: Per-region, reliable
- **Status: Production choice**

### Tesseract 5.4
- Arabic: Reads correctly but variable quality
- Best PSM: 11/12 on raw photos, 6/7 on field crops
- Card number issue: "AS13538" misread as "1513538"
- Preprocessing on raw photos: HURTS accuracy
- Preprocessing on field crops: HELPS (grayscale + Otsu + 2x upscale)
- **Status: Backup option, not primary**

### Surya OCR 0.17.1
- Loaded after fixing transformers version
- Results were poor on CNIE cards
- **Status: Abandoned**

### EasyOCR
- Requires separate PyTorch install (CPU wheel first, THEN easyocr)
- Python 3.13 incompatible
- Slower than PaddleOCR (~300-800ms per crop)
- **Status: Not recommended over PaddleOCR**

---

## 5. Preprocessing — What Helps vs Hurts

### On raw phone photos (full card)
| Method | Effect |
|--------|--------|
| Raw (no preprocessing) | Best baseline |
| Grayscale | Worse |
| Otsu threshold | Much worse — destroys detail |
| Adaptive threshold | Much worse |
| 2x upscale | Amplifies noise |

**Conclusion: Don't preprocess raw full photos.**

### On field crops (isolated regions)
| Method | Effect |
|--------|--------|
| Raw | Baseline |
| Upscale 2x | Helps small text |
| CLAHE | Gentle enhancement, helps uneven lighting |
| CLAHE + adaptive binary | Aggressive, can destroy Arabic thin strokes |

### For the Flask endpoint
We use two modes:
- `raw` — no preprocessing after perspective correction
- `upscale_2x` — `cv2.resize(img, fx=2, fy=2, INTER_CUBIC)` after perspective correction

---

## 6. Architecture — What We Built

```
POST /extract (image file + preprocess=raw|upscale_2x)
    │
    ▼
services/preprocessor.py (EXISTS — 218 lines)
    → Canny edge detection (thresholds: 30, 50, 75)
    → Adaptive threshold fallback
    → Find largest quadrilateral contour (the card)
    → 4-point perspective warp
    → Ensure landscape orientation
    → Resize to 856x540
    │
    ▼
Preprocessing (in app.py)
    raw: no-op
    upscale_2x: cv2.resize 2x INTER_CUBIC
    │
    ▼
services/ocr_engine.py (NEW — 91 lines)
    → run_ocr(image, 'ar') → Arabic detections
    → run_ocr(image, 'fr') → French detections
    │
    ▼
JSON response: raw detections from both models
```

### Files
| File | Lines | Purpose |
|------|-------|---------|
| `app.py` | 84 | Flask endpoint POST /extract |
| `services/ocr_engine.py` | 91 | PaddleOCR singleton + run_ocr() |
| `services/preprocessor.py` | 218 | Card detection + perspective correction |
| `requirements.txt` | 7 | Pinned dependencies |

---

## 7. Language Model Strategy

| Language | Model | What it reads |
|----------|-------|--------------|
| `ar` | PP-OCRv5 Arabic | Arabic script on the card |
| `fr` | PP-OCRv5 French | French + English text (all Latin scripts) |

- No separate English model needed — French model handles all Latin
- Both models run on every request (full image, no field cropping)
- Results returned separately in JSON

---

## 8. Key Decisions & Why

| Decision | Why |
|----------|-----|
| Full image OCR, no field cropping | Field crop coordinates need calibration per card variant. Full image lets PaddleOCR detect everything. |
| Two language models (ar + fr) | PaddleOCR can't mix Arabic + Latin in one instance |
| `.predict()` with file path | Tested in notebook — works reliably. Numpy array input is less stable. |
| Models loaded at import time | Avoids 10-15s load per request |
| Perspective correction keeps 856x540 | Standard ID-1 card size, all field coordinates calibrated to this |
| Python 3.11, not 3.13 | PaddleOCR and PyTorch don't support 3.13 |
| paddlepaddle==3.2.1 exact pin | Tested working. Other versions had DLL errors on Windows. |
| paddleocr==3.4.0 exact pin | Has PP-OCRv5 with Arabic support. Older versions don't. |

---

## 9. Installation Order (CRITICAL)

```bash
# 1. Create Python 3.11 venv
py -3.11 -m venv venv311
venv311\Scripts\activate

# 2. Install paddlepaddle FIRST
pip install paddlepaddle==3.2.1

# 3. Install paddleocr SECOND
pip install paddleocr==3.4.0

# 4. Install the rest
pip install flask opencv-python numpy Pillow

# 5. Optional for notebooks
pip install jupyter ipykernel matplotlib
python -m ipykernel install --user --name=venv311 --display-name="Python 3.11 (OCR)"
```

**Order matters.** paddlepaddle must be installed before paddleocr. If you reverse it, paddleocr pulls in incompatible transitive dependencies.

---

## 10. Testing

```bash
# Start server
python app.py

# Test raw
curl -X POST -F "image=@front.jpeg" http://localhost:5000/extract

# Test with upscale
curl -X POST -F "image=@front.jpeg" -F "preprocess=upscale_2x" http://localhost:5000/extract
```

---

## 11. What's NOT Built Yet

| Component | Status |
|-----------|--------|
| MRZ decoder (back side) | Not implemented |
| Field-to-name mapping | Not implemented (returns raw detections) |
| Cross-validation (MRZ vs visual) | Not implemented |
| Confidence scoring model | Not implemented |
| Back side templates | Not implemented |
| Production deployment | Using Flask dev server |


● Read 1 file (ctrl+o to expand)

● Update(app.py)
  ⎿  Added 2 lines, removed 13 lines
      74      print(f"   DONE in {total_ms}ms")
      75  
      76      return jsonify({
      77 -        "success": True,                                                            
      78 -        "preprocessing": preprocess_mode,                                           
      79 -        "card_detection": {                                                         
      80 -            "method": card_debug.get("detection", "unknown"),                       
      81 -            "original_size": card_debug.get("original_size", "unknown"),            
      82 -            "warped_size": card_debug.get("warped_size", "unknown"),                
      83 -            "ocr_input_size": f"{card_image.shape[1]}x{card_image.shape[0]}",       
      84 -        },                                                                          
      85 -        "results": {                                                                
      86 -            "arabic": ar_results,                                                   
      87 -            "french": fr_results,                                                   
      88 -        },                                                                          
      89 -        "total_time_ms": total_ms,                                                  
      77 +        "arabic": [{"text": d["text"], "confidence": d["confidence"]} for d i       
         +n ar_results["detections"]],                                                        
      78 +        "french": [{"text": d["text"], "confidence": d["confidence"]} for d i       
         +n fr_results["detections"]],                                                        
      79      })
      80  
      81  

● Done. Restart the server and test again — the response is now just:

  {
    "arabic": [
      {"text": "سفيان", "confidence": 0.85},
      ...
    ],
    "french": [
      {"text": "SOUFIANE", "confidence": 0.92},
      ...
    ]
  }