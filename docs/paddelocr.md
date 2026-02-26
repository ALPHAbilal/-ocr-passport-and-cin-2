Here is a complete, production-ready reference for using PaddleOCR on Windows 11 for your CNIE card crops.

***

## 1. Installation (CPU-Only, Windows 11)

Install in this exact order — PaddlePaddle **first**, then PaddleOCR: [paddleocr](https://www.paddleocr.ai/latest/en/version3.x/installation.html)

```bash
# Step 1: PaddlePaddle 3.0.0 CPU (use Baidu index — PyPI version is often stale)
python -m pip install paddlepaddle==3.0.0 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/

# Step 2: PaddleOCR (latest, includes PP-OCRv4 + PP-OCRv5)
python -m pip install paddleocr

# Step 3: Fix known Windows dependency issues
pip install shapely scikit-image "protobuf>=3.20.0,<4.0"
```

Verify PaddlePaddle installed correctly: [paddleocr](https://www.paddleocr.ai/latest/en/version3.x/installation.html)
```bash
python -c "import paddle; print(paddle.__version__)"
# Expected output: 3.0.0
```

***

## 2. Initialize Once → OCR a numpy array

The key is to create **one OCR instance per language** at startup, then reuse it for all crops. Models load on first init (heavy); subsequent calls are fast.

```python
import cv2
import numpy as np
from paddleocr import PaddleOCR

# ── Initialize ONCE per language (do this at notebook startup) ──────────────
# Arabic fields (CIN name, surname in Arabic)
ocr_ar = PaddleOCR(
    use_angle_cls=False,   # no angle classifier needed for flat ID crops
    lang='ar',
    use_gpu=False,
    ocr_version='PP-OCRv4',
    drop_score=0.4,        # discard results below 40% confidence
    show_log=False         # suppress verbose download logs
)

# French / Latin / digits fields
ocr_fr = PaddleOCR(
    use_angle_cls=False,
    lang='fr',
    use_gpu=False,
    ocr_version='PP-OCRv4',
    drop_score=0.4,
    show_log=False
)

# ── OCR a single crop (already a numpy array from OpenCV) ───────────────────
def ocr_crop(ocr_instance, crop_bgr: np.ndarray) -> tuple[str, float]:
    """
    Run recognition only (det=False) on a pre-cropped BGR numpy array.
    Returns (text, confidence).
    """
    result = ocr_instance.ocr(crop_bgr, det=False, rec=True, cls=False)
    # result format when det=False: [[ [text, score], ... ]]
    if result and result[0]:
        texts  = [item[0] for item in result[0]]
        scores = [item [paddleocr](https://www.paddleocr.ai/latest/en/version3.x/installation.html) for item in result[0]]
        return " ".join(texts), min(scores)
    return "", 0.0

# ── Example usage ────────────────────────────────────────────────────────────
# Assuming full_card is already loaded: full_card = cv2.imread("cnie.jpg")
# Crop a field region (y1:y2, x1:x2)
arabic_name_crop = full_card[80:130, 400:750]   # example coords
french_name_crop = full_card[80:130, 50:380]

text_ar, conf_ar = ocr_crop(ocr_ar, arabic_name_crop)
text_fr, conf_fr = ocr_crop(ocr_fr, french_name_crop)

print(f"Arabic  → '{text_ar}'  ({conf_ar:.2f})")
print(f"French  → '{text_fr}'  ({conf_fr:.2f})")
```

> **Output format when `det=False`:** `result[0]` is a list of `[text_str, confidence_float]` pairs — one per detected text line within the crop. For a single-line field (~300×50px), `result[0][0]` holds the single result.

***

## 3. Arabic: Model, Lang Code, and Mixing

PaddleOCR **does** have a dedicated Arabic model. Here's what you need to know: [paddlepaddle.github](https://paddlepaddle.github.io/PaddleOCR/v3.0.2/en/version2.x/ppocr/blog/multi_languages.html)

| Question | Answer |
|---|---|
| Lang code for Arabic | `lang='ar'` |
| Lang code for French | `lang='fr'` |
| Lang code for digits-only | `lang='en'` (most reliable for pure numbers) |
| Arabic + French in ONE call? | **No** — each instance uses one model. Use two instances |
| Arabic script direction | Handled internally — RTL is correctly recognized |
| PP-OCRv4 Arabic accuracy | Good for printed text; weak on connected handwritten Arabic |

**For CNIE fields**, the safest strategy is to route each crop to the right model based on which field it is, since Arabic name fields and French fields are in known fixed positions. [github](https://github.com/PaddlePaddle/PaddleOCR)

> 🔑 **PP-OCRv5 upgrade tip**: PP-OCRv5 (in the same `paddleocr` package) has a new multilingual recognition model covering 109 languages including Arabic, with **40%+ accuracy improvement** on some scripts. You can try `ocr_version='PP-OCRv5'` as a drop-in replacement. [github](https://github.com/PaddlePaddle/PaddleOCR)

***

## 4. Does PaddleOCR Accept numpy arrays?

**Yes, directly.** PaddleOCR's `.ocr()` method accepts: [github](https://github.com/PaddlePaddle/PaddleOCR/discussions/7600)
- A numpy array `(H, W, 3)` — BGR from OpenCV is fine, no RGB conversion needed
- A file path (string)
- A URL

No conversion required. Your OpenCV `crop_bgr` array passes straight in.

***

## 5. Key Parameters Reference

```python
PaddleOCR(
    use_angle_cls=False,  # For pre-cropped flat ID fields: set False (saves ~30ms/call)
                          # Set True only if text might be rotated ±90° or ±180°
    lang='ar',            # 'ar' | 'fr' | 'en' | 'latin'
    use_gpu=False,        # CPU-only
    ocr_version='PP-OCRv4',  # or 'PP-OCRv5' for latest
    drop_score=0.4,       # float [0,1] — drop predictions below this confidence
                          # Lower (0.3) = keep more uncertain results
                          # Higher (0.6) = stricter, fewer false positives
    show_log=False,       # suppress download/init noise in Jupyter
    rec_char_type=None,   # Deprecated in v2.x — ignored when lang= is set. Don't use.
)
```

When calling `.ocr()`:
```python
ocr.ocr(crop, det=False, rec=True, cls=False)
#              ^^^^^^^^^ KEY: disables text detection box finding
#                              ^^^^^^^^^^ enables recognition
#                                          ^^^^^^^^^ disables angle classifier
```

***

## 6. Disabling Detection (`det=False`)

**Yes, fully supported**. Since you already have precise crops: [github](https://github.com/PaddlePaddle/PaddleOCR/discussions/7600)

```python
# det=False → skips the DB text detection network entirely
# The entire crop image is treated as a SINGLE text line/region
result = ocr.ocr(crop, det=False, rec=True, cls=False)
```

This is the correct and intended pattern for pre-cropped images. Detection is the slowest stage (~200–500ms per image); skipping it brings per-crop time down to **20–80ms** on CPU.

**One caveat**: with `det=False`, if your crop contains **multiple lines** (e.g., a field that wraps), PaddleOCR may only return the first line. If that's a concern, use a small `det=True` pass or pre-split your crop by line height.

***

## 7. Windows Installation Pitfalls

| Pitfall | Fix |
|---|---|
| `protobuf` version conflict (most common) | `pip install "protobuf>=3.20.0,<4.0"` |
| `ImportError: DLL load failed` for paddlepaddle | Install [Visual C++ 2019 Redistributable](https://aka.ms/vs/16/release/vc_redist.x64.exe) |
| `paddlepaddle` from PyPI is outdated/wrong build | Always use Baidu index: `-i https://www.paddlepaddle.org.cn/packages/stable/cpu/`  [paddleocr](https://www.paddleocr.ai/latest/en/version3.x/installation.html) |
| `shapely` missing (polygon geometry) | `pip install shapely` |
| Mismatched versions (`paddlepaddle` 2.x + `paddleocr` 3.x) | PaddleOCR 3.x **requires** PaddlePaddle 3.x — don't mix |
| Long Windows path errors | Enable long paths: `HKLM\SYSTEM\CurrentControlSet\Control\FileSystem\LongPathsEnabled = 1` |
| First run downloads models slowly | Models are cached in `~/.paddleocr/` — one-time download of ~10–40MB per lang |
| Jupyter kernel crashes on init | Run PaddleOCR init in a **separate cell** before your inference cells |

***

## 8. Expected Processing Time per Crop (CPU)

For a `~300×50px` crop on a modern CPU (recognition only, `det=False`):

| Stage | Time |
|---|---|
| First `.ocr()` call (warm-up) | 500ms – 2s (JIT + model load) |
| Subsequent calls (same instance) | **20 – 80ms** per crop |
| With `det=True` (full pipeline) | 300 – 800ms per crop |
| Angle classifier (`cls=True`) | +30 – 60ms overhead |

For a CNIE with ~8–10 fields, expect **total processing under 1 second** after the first warm-up call, processing all crops sequentially. PaddleOCR uses Intel MKL-DNN acceleration on CPU automatically via paddlepaddle. [arxiv](https://arxiv.org/pdf/2109.15099.pdf)