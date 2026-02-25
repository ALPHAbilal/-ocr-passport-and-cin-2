Here is a complete, production-ready reference covering every aspect of your PaddleOCR setup.

***

## Version Compatibility (Pick One Track)

PaddleOCR 3.x completely broke backwards compatibility with 2.x — they use different APIs. Choose one track and stay consistent. [pypi](https://pypi.org/project/paddleocr/)

| Track | PaddleOCR | PaddlePaddle | Python | API Method | Notes |
|---|---|---|---|---|---|
| **A (Stable/Legacy)** | `2.7.3` | `2.6.1` | 3.10 | `ocr.ocr()` | Most tutorial-compatible, stable on Windows |
| **B (Modern, recommended)** | `3.0.3` | `3.0.0` | 3.10 | `ocr.predict()` | Better multilingual, Arabic, 109 langs |
| Avoid | 3.2.0+ | 3.1.x+ | 3.11 | — | NumPy 2.x module compilation errors on Windows  [github](https://github.com/PaddlePaddle/PaddleOCR/discussions/16341) |

**Recommendation: Use Track A for immediate Flask deployment.** Python 3.10 is the sweet spot — 3.11 has known compiled-module issues with both tracks, and 3.12 had strict numpy/pandas restrictions until PaddleOCR 3.0.2. [pypi](https://pypi.org/project/paddleocr/)

***

## Installation (Track A — Copy-Paste Ready)

### Step 1: Create a clean virtual environment

```bash
python -m venv venv_ocr
venv_ocr\Scripts\activate   # Windows
```

### Step 2: Install PaddlePaddle CPU-only

```bash
# Track A — from standard PyPI
pip install paddlepaddle==2.6.1

# Track B — from Paddle's own index (REQUIRED for 3.x)
# pip install paddlepaddle==3.0.0 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/
```

### Step 3: Install PaddleOCR (basic only — no Chinese NLP!)

```bash
# Track A — basic install, NO paddlenlp, NO Chinese tokenizers
pip install paddleocr==2.7.3

# Track B equivalent (do NOT use [all] — that pulls in NLP junk)
# pip install paddleocr==3.0.3
```

The `paddleocr[all]` tag installs `paddlenlp`, `lmdb`, `sentencepiece`, layout analysis models, and more. For pure OCR, never use `[all]`. Just `pip install paddleocr` gives you detection + recognition + angle classifier — nothing else. [pypi](https://pypi.org/project/paddleocr/)

### Step 4: Pin conflict-prone dependencies

```bash
pip install "numpy==1.26.4"
pip install "protobuf==3.20.3"
pip install "opencv-contrib-python==4.8.0.76"
pip install "Pillow==10.2.0"
```

**Never install both `opencv-python` AND `opencv-contrib-python`** — they share file names and create version clashes. If one is already installed: [github](https://github.com/PaddlePaddle/PaddleOCR/issues/11555)
```bash
pip uninstall opencv-python opencv-contrib-python -y
pip install opencv-contrib-python==4.8.0.76
```

### Full requirements.txt (Track A, Windows CPU)

```text
paddlepaddle==2.6.1
paddleocr==2.7.3
numpy==1.26.4
protobuf==3.20.3
opencv-contrib-python==4.8.0.76
Pillow==10.2.0
Flask==3.0.3
```

***

## Known Conflicts and Fixes

| Error | Cause | Fix |
|---|---|---|
| `protobuf` version conflict | onnx needs `>=3.20.2`, paddle needs `<=3.20.0` | `pip install protobuf==3.20.3` — the patch release satisfies both  [github](https://github.com/PaddlePaddle/PaddleOCR/issues/9468) |
| `numpy.bool` DeprecationError | numpy≥1.24 removed `np.bool` alias | Pin `numpy==1.26.4` (or upgrade to PaddleOCR 3.x)  [github](https://github.com/PaddlePaddle/PaddleOCR/issues/9468) |
| `cv2.error` at import | Both opencv packages installed | Uninstall both, reinstall only `opencv-contrib-python`  [github](https://github.com/PaddlePaddle/PaddleOCR/issues/11555) |
| `dnnl::error` / OneDNN crash in Flask | Flask multiprocessing conflicts with Intel OneDNN | Run Flask with `threaded=True, processes=1` (see Flask section)  [giters](https://giters.com/PaddlePaddle/PaddleOCR/issues/3753) |
| `A module was compiled with a different version` | Python 3.11 + numpy mismatch in 3.x | Use Python 3.10  [github](https://github.com/PaddlePaddle/PaddleOCR/discussions/16341) |

***

## ID Card OCR Configuration

### (a) MRZ Lines — OCR-B Latin Font

For MRZ, **skip detection entirely**. The lines are perfectly aligned, fixed-width, in OCR-B font. Running the detection model wastes 80% of your inference time on pre-cropped regions.

```python
ocr_mrz = PaddleOCR(
    use_angle_cls=False,   # MRZ is already horizontal — no need
    lang='en',             # Latin/OCR-B only
    use_gpu=False,
    show_log=False,
    rec_model_dir='./models/rec/en',   # local path (see pre-download section)
    det_model_dir='./models/det/en',
    # Tuned for small crops
    det_db_thresh=0.3,
    det_db_box_thresh=0.5,
    det_db_unclip_ratio=1.5,   # smaller → tighter boxes on pre-cropped
    rec_batch_num=1,            # single line, batch size 1
)

# For pre-cropped MRZ image, skip detection:
result = ocr_mrz.ocr(mrz_img, det=False, rec=True, cls=False)
text = result[0][0][0]  # just the string
```

For MRZ specifically, also consider the dedicated [`mrz`](https://pypi.org/project/mrz/) library (`pip install mrz`) — it's purpose-built for ICAO TD1/TD3 format parsing with checksum validation, far more reliable than general OCR for this specific task.

### (b) Mixed Arabic + French Text

PaddleOCR 2.x does **not** support mixed scripts in a single model pass. You need two separate instances. PaddleOCR 3.x's PP-OCRv5 supports Arabic script natively in its multilingual model as of 3.3.0. [stackoverflow](https://stackoverflow.com/questions/79540177/paddleocr-ocr-analyzes-left-to-right-instead-of-right-to-left-for-arabic-how-to)

```python
ocr_latin = PaddleOCR(
    use_angle_cls=False,
    lang='en',          # French uses Latin alphabet — 'en' model covers it
    use_gpu=False,
    show_log=False,
    rec_batch_num=6,
)

ocr_arabic = PaddleOCR(
    use_angle_cls=False,  # False for pre-aligned, cropped fields
    lang='ar',
    use_gpu=False,
    show_log=False,
    rec_batch_num=6,
)
```

**Important Arabic RTL caveat**: PaddleOCR returns Arabic text in left-to-right word order regardless of language. You must reverse the word order post-recognition: [stackoverflow](https://stackoverflow.com/questions/79540177/paddleocr-ocr-analyzes-left-to-right-instead-of-right-to-left-for-arabic-how-to)

```python
def fix_arabic_rtl(text: str) -> str:
    words = text.split()
    return ' '.join(reversed(words))
```

### Memory cost of two instances

Each loaded PaddleOCR 2.x mobile model uses ~200–350MB RAM. Two instances (en + ar) = ~500–700MB combined. Server-grade models double that. For Flask on a VPS, mobile models are the right choice.

### `use_angle_cls` decision

| Scenario | Setting |
|---|---|
| Pre-cropped, aligned field (known orientation) | `use_angle_cls=False` — saves ~30% inference time |
| Full ID card image, unknown orientation | `use_angle_cls=True` |
| MRZ zone (always horizontal) | `use_angle_cls=False` |

### Detection parameters for small crops (~300×50px)

For single-field crops, **the best option is to bypass detection entirely** with `det=False`. If you must detect:

```python
# These values work well for tight, small crops
det_db_thresh=0.3          # default; lower to 0.2 if text is missed
det_db_box_thresh=0.5      # default
det_db_unclip_ratio=1.5    # smaller than default 2.0 for tight regions
```

***

## Flask: Singleton, Logs, and Pre-Download

### Singleton pattern

Initialize at app start — never inside a request handler: [giters](https://giters.com/PaddlePaddle/PaddleOCR/issues/3753)

```python
# ocr_service.py
import os
import logging
os.environ['FLAGS_call_stack_level'] = '2'  # reduce paddle C++ verbosity

from paddleocr import PaddleOCR

logging.getLogger('ppocr').setLevel(logging.ERROR)  # suppress ppocr INFO spam

_ocr_latin: PaddleOCR | None = None
_ocr_arabic: PaddleOCR | None = None

def get_ocr_latin() -> PaddleOCR:
    global _ocr_latin
    if _ocr_latin is None:
        _ocr_latin = PaddleOCR(
            use_angle_cls=False,
            lang='en',
            use_gpu=False,
            show_log=False,
            det_model_dir='./models/det/en',
            rec_model_dir='./models/rec/en',
            cls_model_dir='./models/cls',
        )
    return _ocr_latin

def get_ocr_arabic() -> PaddleOCR:
    global _ocr_arabic
    if _ocr_arabic is None:
        _ocr_arabic = PaddleOCR(
            use_angle_cls=False,
            lang='ar',
            use_gpu=False,
            show_log=False,
            det_model_dir='./models/det/ml',
            rec_model_dir='./models/rec/ar',
        )
    return _ocr_arabic
```

```python
# app.py
from flask import Flask, request, jsonify
from ocr_service import get_ocr_latin, get_ocr_arabic
import numpy as np
import cv2

app = Flask(__name__)

# Warm up at startup — this triggers model loading ONCE
with app.app_context():
    get_ocr_latin()
    get_ocr_arabic()

@app.route('/ocr/mrz', methods=['POST'])
def ocr_mrz():
    file = request.files['image']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    result = get_ocr_latin().ocr(img, det=False, rec=True, cls=False)
    lines = [item[0] for item in result[0]] if result[0] else []
    return jsonify({'lines': lines})

@app.route('/ocr/arabic', methods=['POST'])
def ocr_arabic_field():
    file = request.files['image']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    result = get_ocr_arabic().ocr(img, det=True, rec=True, cls=False)
    texts = []
    if result[0]:
        for box, (text, score) in result[0]:
            words = text.split()
            texts.append(' '.join(reversed(words)))  # fix RTL
    return jsonify({'texts': texts})

if __name__ == '__main__':
    # Single process — critical to avoid OneDNN/Flask multiprocess crash
    app.run(host='0.0.0.0', port=5000, threaded=True, processes=1)
```

### Suppressing startup logs

Three layers of suppression are needed — Paddle logs come from both Python and C++: [blog.csdn](https://blog.csdn.net/u013066730/article/details/121423704)

```python
import os
import logging

# 1. Suppress C++ Paddle glog output
os.environ['FLAGS_call_stack_level'] = '2'
os.environ['GLOG_v'] = '0'
os.environ['GLOG_logtostderr'] = '0'

# 2. Suppress Python logging
logging.getLogger('ppocr').setLevel(logging.ERROR)
logging.getLogger('paddle').setLevel(logging.ERROR)

# 3. show_log=False in constructor
ocr = PaddleOCR(use_angle_cls=False, lang='en', use_gpu=False, show_log=False)
```

For the remaining C++ IR optimization logs (`Fused 0 subgraphs`, `skip [feed]`), you need to patch PaddleOCR's `utility.py`: [blog.csdn](https://blog.csdn.net/u013066730/article/details/121423704)

```python
# In venv/Lib/site-packages/paddleocr/tools/infer/utility.py
# Find this block and uncomment config.disable_glog_info():
config.enable_memory_optim()
config.disable_glog_info()           # ← uncomment this line
config.switch_ir_optim(False)        # ← change True to False
```

### Pre-downloading models (prevent runtime downloads)

Run this **once** before deploying to production:

```python
# preload_models.py — run once to cache all models locally
from paddleocr import PaddleOCR

print("Downloading English/Latin models...")
PaddleOCR(use_angle_cls=False, lang='en', use_gpu=False, show_log=False)

print("Downloading Arabic models...")
PaddleOCR(use_angle_cls=False, lang='ar', use_gpu=False, show_log=False)

print("Done. Models cached at: C:/Users/<you>/.paddleocr/")
```

To point Flask to a local model directory (offline deployment):

```python
ocr = PaddleOCR(
    det_model_dir='C:/myapp/models/det/en_PP-OCRv3_det_infer',
    rec_model_dir='C:/myapp/models/rec/en_PP-OCRv4_rec_infer',
    cls_model_dir='C:/myapp/models/cls/ch_ppocr_mobile_v2.0_cls_infer',
    lang='en',
    use_gpu=False,
    show_log=False,
)
```

The model folders are at `C:\Users\<you>\.paddleocr\whl\` after first download.

***

## Complete Minimal Script

```python
"""
Minimal PaddleOCR script — Track A (paddleocr==2.7.3, paddlepaddle==2.6.1)
Usage: python ocr_minimal.py path/to/image.jpg
"""
import os
import sys
import logging

# Silence before any paddle imports
os.environ['FLAGS_call_stack_level'] = '2'
os.environ['GLOG_v'] = '0'
logging.getLogger('ppocr').setLevel(logging.ERROR)

import cv2
import numpy as np
from paddleocr import PaddleOCR

def build_ocr(lang: str = 'en') -> PaddleOCR:
    return PaddleOCR(
        use_angle_cls=False,
        lang=lang,
        use_gpu=False,
        show_log=False,
        rec_batch_num=6,
        det_db_thresh=0.3,
        det_db_box_thresh=0.5,
    )

# Initialize ONCE
ocr_en = build_ocr('en')
ocr_ar = build_ocr('ar')

def run_ocr(image_path: str, lang: str = 'en', skip_det: bool = False):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Cannot open: {image_path}")

    engine = ocr_en if lang == 'en' else ocr_ar
    result = engine.ocr(img, det=not skip_det, rec=True, cls=False)

    lines = []
    if result and result[0]:
        for item in result[0]:
            if skip_det:
                text, score = item[0], item [pypi](https://pypi.org/project/paddleocr/)
            else:
                _, (text, score) = item
            lines.append({'text': text, 'score': round(score, 4)})
    return lines

if __name__ == '__main__':
    path = sys.argv [pypi](https://pypi.org/project/paddleocr/) if len(sys.argv) > 1 else 'test.jpg'

    print("=== Latin/MRZ (no detection) ===")
    for item in run_ocr(path, lang='en', skip_det=True):
        print(f"  {item['text']} ({item['score']})")

    print("\n=== Arabic (with detection) ===")
    for item in run_ocr(path, lang='ar', skip_det=False):
        words = item['text'].split()
        rtl_text = ' '.join(reversed(words))
        print(f"  {rtl_text} ({item['score']})")
```

***

## OCR Tool Comparison for ID Cards

| Tool | MRZ Accuracy | Arabic | French | Install Size | CPU Speed | Verdict |
|---|---|---|---|---|---|---|
| **PaddleOCR** | Good (needs tuning) | ✅ `lang='ar'` | ✅ `lang='en'` | ~1.5GB | 100–300ms | Best all-rounder |
| **EasyOCR** | Good | ✅ native RTL | ✅ | ~1.2GB | 400–800ms | Better Arabic accuracy  [tildalice](https://tildalice.io/ocr-tesseract-easyocr-paddleocr-benchmark/) |
| **Tesseract** | Excellent (OCR-B trained) | ⚠️ poor | ✅ | ~50MB | ~50ms | Best for MRZ only |
| **`mrz` library** | Excellent + checksum | N/A (MRZ only) | N/A | ~5MB | <10ms | **Use this for MRZ** |

**Recommended hybrid strategy for Moroccan ID cards:**
- Use [`mrz`](https://pypi.org/project/mrz/) (`pip install mrz`) for the MRZ zone — it validates TD1/TD3 checksums automatically
- Use PaddleOCR with `lang='ar'` for the Arabic body fields
- Use PaddleOCR with `lang='en'` (or EasyOCR) for French fields

***

## Performance

CPU inference times on a ~300×50px crop (Windows, no GPU): [tildalice](https://tildalice.io/ocr-tesseract-easyocr-paddleocr-benchmark/)

| Config | Det + Rec | Rec Only (skip det) |
|---|---|---|
| PP-OCRv3 mobile | ~150–250ms | ~30–60ms |
| PP-OCRv4 mobile | ~200–350ms | ~40–80ms |
| Two instances initialized | +0ms (singleton) | — |

Model memory footprint (loaded into RAM):

| Model | Disk | RAM |
|---|---|---|
| Mobile detection (en) | ~2.4MB | ~80MB |
| Mobile recognition (en) | ~4.8MB | ~120MB |
| Mobile recognition (ar) | ~4.8MB | ~120MB |
| Total (en + ar, no cls) | ~12MB | ~400MB |

To get faster inference, skip detection on pre-cropped fields (`det=False`) — that alone cuts latency by ~60–70% for small crops. There are no official quantized/INT8 lite models for CPU in the Python pip package; ONNX Runtime export is available in PaddleOCR 3.x for further acceleration. [pypi](https://pypi.org/project/paddleocr/)