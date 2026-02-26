Here's a comprehensive breakdown covering every aspect of your requirements for Arabic + French ID card OCR on CPU-only in 2025/2026.

***

## Best CPU-Friendly OCR Solutions

### 1. Surya OCR (Top Open-Source Pick)

Surya is currently the best open-source option for multilingual document OCR and supports 90+ languages including Arabic and French. It runs on CPU (Linux/Windows), though significantly slower than GPU mode. Its architecture is based on a **modified Donut model** with GQA and MoE layers, benchmarking at **0.97 avg similarity** vs Tesseract's 0.88. [pypi](https://pypi.org/project/surya-ocr/0.2.0/)

```bash
pip install surya-ocr
```

```python
from surya.ocr import run_ocr
from surya.model.detection.model import load_model as load_det
from surya.model.recognition.model import load_model as load_rec
from PIL import Image

image = Image.open("id_card.jpg")
langs = ["ar", "fr"]
det_model, det_processor = load_det()
rec_model, rec_processor = load_rec()

predictions = run_ocr([image], [langs], det_model, det_processor, rec_model, rec_processor)
```

> **GitHub:** [datalab-to/surya](https://github.com/datalab-to/surya) [github](https://github.com/datalab-to/surya)

***

### 2. Surya + Docling Pipeline (Structured Output)

Combining **Surya OCR** with **Docling** gives you layout-aware, structured document parsing — ideal for ID cards where field positions matter. Docling acts as an orchestration layer that converts Surya's raw detections into a coherent document schema. [dev](https://dev.to/aairom/using-suryaocr-with-docling-1d9k)

```bash
pip install docling surya-ocr
```

Docling also has a GitHub issue specifically tracking Arabic scanned document support as of February 2026. [github](https://github.com/docling-project/docling/issues/3021)

***

### 3. MRZ-Specific Libraries

For the MRZ zone, use dedicated parsers rather than generic OCR:

| Library | GitHub | Notes |
|---|---|---|
| `readmrz` | [egemenzeytinci/readmrz](https://github.com/egemenzeytinci/readmrz) | Detects + crops + reads MRZ, pure Python  [github](https://github.com/egemenzeytinci/readmrz) |
| `mrz` (PyPI) | `pip install mrz` | ICAO 9303 standard, generator + checker for TD1/TD3  [pypi](https://pypi.org/project/mrz/) |
| `MRZScanner` | [DocsaidLab/MRZScanner](https://github.com/DocsaidLab/MRZScanner) | Trained model for visas, passports, ID cards  [github](https://github.com/DocsaidLab/MRZScanner) |

```python
# readmrz example
from readmrz import MrzDetector, MrzReader
detector = MrzDetector()
reader = MrzReader()
image = detector.read('id_card.jpg')
cropped = detector.crop_area(image)
result = reader.process(cropped)  # Returns structured dict
```

MRZ text uses only ASCII characters, so any OCR works reliably on it — the real challenge is detection and cropping.

***

## Cloud APIs (Highest Accuracy, No GPU Required)

For a 9/10+ accuracy bar on Arabic + French, cloud APIs are the safest bet: [research.aimultiple](https://research.aimultiple.com/ocr-accuracy/)

| API | Arabic+French Accuracy | MRZ Support | Cost |
|---|---|---|---|
| **Mistral OCR 3** | 99%+ on 25+ languages, 96.6% on tables | Via text extraction | Pay-per-use  [jannikreinhard](https://jannikreinhard.com/2026/01/12/master-the-paper-chaos-comparing-azures-ocr-and-document-intelligence-powerhouses/) |
| **Google Cloud Vision** | ~98% overall, top benchmark performer | Yes (Document Text Detection) | $1.50/1K images  [photes](https://photes.io/blog/posts/ocr-research-trend) |
| **Azure Document Intelligence** | 96% on printed text | Yes | Pay-per-use  [research.aimultiple](https://research.aimultiple.com/ocr-accuracy/) |
| **AWS Textract** | ~95%, strong on structured docs | Yes | Pay-per-use  [research.aimultiple](https://research.aimultiple.com/ocr-accuracy/) |

**Mistral OCR** (`mistral-ocr-latest`) is the 2025/2026 standout for Arabic specifically, outperforming traditional OCR tools by 60% CER on Arabic benchmarks: [arxiv](https://arxiv.org/html/2502.14949v1)

```python
from mistralai import Mistral
import base64

client = Mistral(api_key="YOUR_API_KEY")
with open("id_card.jpg", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode()

response = client.ocr.process(
    model="mistral-ocr-latest",
    document={"type": "image_url", "image_url": f"data:image/jpeg;base64,{img_b64}"}
)
print(response.pages[0].markdown)
```

***

## Lightweight Transformer Models on CPU

**TrOCR** (Microsoft) runs on CPU but is slow (~5–15s/image) and has no native Arabic support without fine-tuning. The **HATFormer** model (Arabic-specific TrOCR adaptation) achieves strong CER but requires fine-tuning effort. [arxiv](https://arxiv.org/html/2410.02179v2)

For a Hugging Face model ready for CPU deployment:

```python
# Qwen2-VL-2B — small VLM, decent Arabic OCR, CPU-runnable (slow ~20-60s)
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
model = Qwen2VLForConditionalGeneration.from_pretrained("Qwen/Qwen2-VL-2B-Instruct")
```

Modern VLMs (GPT-4o, Gemini, Qwen) outperform traditional OCR tools by **60% CER** on Arabic benchmarks, but they're either API-only or slow on CPU. [arxiv](https://arxiv.org/html/2502.14949v2)

***

## ONNX / Quantized Models for CPU Speed

- **PaddleOCR ONNX**: The HuggingFace repo [`monkt/paddleocr-onnx`](https://huggingface.co/monkt/paddleocr-onnx) provides ONNX-converted PaddleOCR models for production CPU deployment without PaddlePaddle dependency conflicts [huggingface](https://huggingface.co/monkt/paddleocr-onnx)
- **PP-OCRv2** (lightweight backbone LCNet) was specifically designed for ultra-lightweight CPU inference — 7% better precision than PP-OCR at the same inference cost [arxiv](https://arxiv.org/pdf/2109.03144.pdf)

```bash
pip install onnxruntime  # CPU-only, no CUDA needed
# Use monkt/paddleocr-onnx for drop-in replacement
```

***

## Arabic OCR Preprocessing Pipeline

This is where you gain the most accuracy — models + preprocessing are what separate 7/10 from 9/10+: [linkedin](https://www.linkedin.com/posts/ramzy-kemmoun-1a3725237_arabicocr-deeplearning-imageprocessing-activity-7397377919339110402-B0BO)

1. **Deskew & orientation correction** — ensures text lines are horizontal (use `opencv-python` + Hough transform or `deskew` library)
2. **Noise removal** — Median filter or bilateral Gaussian blur to remove scan artifacts
3. **Adaptive thresholding** — `cv2.adaptiveThreshold` with Gaussian method outperforms global binarization for varying-light ID scans
4. **ROI cropping** — isolate Arabic text zones from French zones and MRZ zone separately, then feed each region to its OCR engine
5. **Contrast enhancement** — CLAHE (Contrast Limited Adaptive Histogram Equalization) via `cv2.createCLAHE()`
6. **Resolution upscaling** — resize to minimum 300 DPI equivalent before OCR (upscale if source is low-res)

```python
import cv2
import numpy as np

def preprocess_id_card(img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    denoised = cv2.medianBlur(enhanced, 3)
    binary = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY, 11, 2)
    return binary
```

***

## Recommended Architecture for Your Use Case

Given your context (Moroccan ID cards, Arabic + French, CPU-only, 9/10 accuracy target):

```
Image Input
    ↓
Preprocessing (OpenCV: deskew, CLAHE, denoise)
    ↓
Zone Detection (split Arabic / French / MRZ regions)
    ↓
┌─────────────────────────────────────┐
│  Arabic zones → Mistral OCR API     │  ← 99%+ accuracy
│  French zones → Surya OCR (CPU)     │  ← 97% similarity
│  MRZ zone    → readmrz library      │  ← near 100% with good crop
└─────────────────────────────────────┘
    ↓
JSON structured output
```

If fully offline is required, use **Surya OCR for all text** + `readmrz` for MRZ. If you can accept API calls, **Mistral OCR** is the highest-accuracy Arabic solution available in 2025/2026. [jannikreinhard](https://jannikreinhard.com/2026/01/12/master-the-paper-chaos-comparing-azures-ocr-and-document-intelligence-powerhouses/)