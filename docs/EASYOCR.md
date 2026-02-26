Here's a complete, production-ready guide for your CNIE pipeline on Windows 11.

***

## 1. Installation (Windows CPU-Only)

**Step 1 — Install PyTorch CPU first** (mandatory on Windows before EasyOCR): [pypi](https://pypi.org/project/easyocr/)

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

**Step 2 — Then install EasyOCR:**

```bash
pip install easyocr opencv-python
```

> ⚠️ **Python version**: Use Python **3.10 or 3.11**. Python 3.13 causes `ModuleNotFoundError: No module named 'torch.backends'` with EasyOCR on Windows 11 and is currently unsupported. [discuss.pytorch](https://discuss.pytorch.org/t/modulenotfounderror-no-module-named-torch-backends-with-easyocr-and-python-3-13-windows-11-exhaustive-troubleshooting-still-stuck/216718)

***

## 2. Critical: Arabic ≠ Latin — Use Two Readers

Arabic and French/English use **different internal recognition models** and are **not compatible in a single reader**.  You must initialize two readers — once each, at startup — and route each crop accordingly: [github](https://github.com/JaidedAI/EasyOCR)

```python
import easyocr

# Initialize ONCE at startup — expensive step, ~5–10s per reader on CPU
reader_arabic = easyocr.Reader(['ar'], gpu=False)
reader_latin  = easyocr.Reader(['fr', 'en'], gpu=False)
```

This is a hard architectural constraint: "Languages that share most characters (e.g. Latin script) with each other are compatible." Arabic shares no characters with French/English. [jaided](https://www.jaided.ai/easyocr/tutorial/)

***

## 3. Minimal Working Code (NumPy Array, No File Path)

EasyOCR's `image` parameter officially accepts **"string, numpy array, byte"** — your OpenCV BGR crop passes directly: [jaided](http://www.jaided.ai/easyocr/documentation/)

```python
import easyocr
import cv2

# Assume: crop is a NumPy array (H, W, 3) in BGR from cv2.imread or slicing

# --- For an Arabic-only field ---
def ocr_arabic(crop):
    results = reader_arabic.readtext(
        crop,                    # OpenCV numpy array accepted directly
        detail=0,                # Returns list of strings only (no bbox/conf)
        paragraph=False,         # Keep lines separate for structured fields
        decoder='beamsearch',    # More accurate than greedy for Arabic
        beamWidth=5,
    )
    return ' '.join(results)

# --- For a French/digits field ---
def ocr_latin(crop, digits_only=False):
    allowlist = '0123456789' if digits_only else None
    results = reader_latin.readtext(
        crop,
        detail=0,
        paragraph=False,
        decoder='greedy',        # Greedy is faster; fine for Latin + digits
        allowlist=allowlist,     # Restrict to digits when field is digits-only
    )
    return ' '.join(results)
```

***

## 4. Does EasyOCR Accept NumPy Arrays Directly?

**Yes.** The official `readtext` signature is: [pypi](https://pypi.org/project/easyocr/1.1.4/)

```
image (string, numpy array, byte) — Input image
```

No conversion to PIL is needed. OpenCV's BGR format is handled internally — EasyOCR converts it before passing to the model. Do **not** call `cv2.cvtColor` unless you want to preprocess contrast yourself.

***

## 5. Key Accuracy Parameters

| Parameter | Default | Recommendation for CNIE crops |
|---|---|---|
| `decoder` | `'greedy'` | Use `'beamsearch'` for Arabic; `'greedy'` is fine for Latin/digits  [jaided](http://www.jaided.ai/easyocr/documentation/) |
| `beamWidth` | `5` | Increase to `10` for Arabic if accuracy is low (slower)  [jaided](http://www.jaided.ai/easyocr/documentation/) |
| `detail` | `1` | Set to `0` for clean string output per-field  [blog.roboflow](https://blog.roboflow.com/how-to-use-easyocr/) |
| `paragraph` | `False` | Keep `False` for single-line field crops  [jaided](http://www.jaided.ai/easyocr/documentation/) |
| `allowlist` | `None` | Use `'0123456789'` for DOB, ID number fields  [jaided](http://www.jaided.ai/easyocr/documentation/) |
| `contrast_ths` | `0.1` | Leave default; raise to `0.3` if ID card has faded text  [jaided](http://www.jaided.ai/easyocr/documentation/) |
| `adjust_contrast` | `0.5` | Pairs with `contrast_ths` for low-contrast scans  [jaided](http://www.jaided.ai/easyocr/documentation/) |
| `min_size` | `10` | Lower to `5` if small characters are missed on 300×50px crops  [jaided](http://www.jaided.ai/easyocr/documentation/) |
| `mag_ratio` | `1` | Try `1.5`–`2.0` on very small crops to upscale before detection  [jaided](http://www.jaided.ai/easyocr/documentation/) |

For small crops (~300×50px), `paragraph=False` is critical — `True` tries to merge lines and may collapse multi-token fields incorrectly.

***

## 6. Common Windows Errors and Fixes

- **`ModuleNotFoundError: No module named 'torch.backends'`** — Python 3.13 incompatibility. Downgrade to Python 3.10/3.11. [discuss.pytorch](https://discuss.pytorch.org/t/modulenotfounderror-no-module-named-torch-backends-with-easyocr-and-python-3-13-windows-11-exhaustive-troubleshooting-still-stuck/216718)
- **`Neither CUDA nor MPS are available`** warning — This is just a warning, not an error. It appears when you don't pass `gpu=False` explicitly. Always pass `gpu=False` to silence it and avoid any GPU probe. [github](https://github.com/JaidedAI/EasyOCR/issues/1304)
- **EasyOCR installs CUDA-linked PyTorch** — happens if you `pip install easyocr` without pre-installing the CPU wheel. EasyOCR's dependency resolver pulls the default torch, which may be CUDA-linked and much larger (~2 GB). Always install the CPU wheel first with the `--index-url` flag. [jaided](https://www.jaided.ai/easyocr/install/)
- **Model download fails silently** — First `Reader()` call downloads CRAFT + recognition models to `~/.EasyOCR/`. Ensure internet access on first init, or pre-download and set `model_storage_directory`. [jaided](http://www.jaided.ai/easyocr/documentation/)
- **`pip` version mismatch** — Run `python -m pip install --upgrade pip` before installing to avoid resolver conflicts. [github](https://github.com/JaidedAI/EasyOCR/issues/1304)

***

## 7. Expected Processing Time per Crop (CPU)

| Phase | Time on CPU |
|---|---|
| `Reader()` initialization (per reader) | ~5–15 seconds (one-time)  [github](https://github.com/JaidedAI/EasyOCR/issues/88) |
| First `readtext()` call | ~1–3 seconds (JIT warmup) |
| Subsequent calls on ~300×50px crops | **~0.3–0.8 seconds** per crop  [stackoverflow](https://stackoverflow.com/questions/73431716/i-am-trying-to-run-inference-on-a-single-gpu-with-easyocr-i-have-tried-running) |
| With `decoder='beamsearch'` | ~1.5× slower than greedy |

The ~0.34s GPU benchmark from a 512×384 image translates to roughly **0.5–1.5 seconds on CPU** for your 300×50px crops — detection (CRAFT) dominates, not recognition. To speed up a full card pipeline, consider calling `reader.detect()` once on the full crop then `reader.recognize()` per region, rather than `readtext()` on each isolated crop. [stackoverflow](https://stackoverflow.com/questions/73431716/i-am-trying-to-run-inference-on-a-single-gpu-with-easyocr-i-have-tried-running)