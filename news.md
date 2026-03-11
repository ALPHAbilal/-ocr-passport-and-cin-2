Here's a comprehensive breakdown of each of your five questions, grounded in PP-OCRv5's actual architecture and the Arabic recognition model specifics.

***

## 1. Input Resolution: Is 856×540 Too Small?

Your 856×540 warped card image is **borderline sufficient but not optimal** for PP-OCRv5 Arabic recognition. The PP-OCRv5 recognition model internally resizes each detected text line crop to a fixed height of **48 pixels** before feeding it to the backbone. At 540px card height with typical CNIE text lines occupying ~20–30px, your per-character pixel density is very tight — Arabic dots and diacritics that distinguish ر/ن (a single dot) and غ/ع (a dot above) need at least 8–10px per character height to survive the resize. [paddleocr](https://www.paddleocr.ai/latest/en/version3.x/pipeline_usage/OCR.html)

**Recommendation:** Yes, **2× upscaling to 1712×1080 is worthwhile**. PP-OCRv5's documentation benchmarks configurations with `text_det_limit_side_len=1280` and `limit_type=min`, which means the model expects a minimum short side of 1280px — your 540px is well below that. Use `cv2.resize` with `INTER_CUBIC` or `INTER_LANCZOS4` interpolation before feeding to OCR: [paddleocr](https://www.paddleocr.ai/latest/en/version3.x/algorithm/PP-OCRv5/PP-OCRv5.html)

```python
img_2x = cv2.resize(warped, (1712, 1080), interpolation=cv2.INTER_CUBIC)
```

***

## 2. JPEG Compression vs. Numpy Array Direct Input

**JPEG compression is a real problem for Arabic.** JPEG's 8×8 DCT block compression creates ringing artifacts around high-frequency edges — precisely the thin strokes and dot positions (nuqat) that distinguish ر/ن, غ/ع, ب/ت/ث. At quality=95+ the loss is minimal, but default JPEG quality (often 75–85) will meaningfully degrade dots. [paddleocr](https://www.paddleocr.ai/latest/en/version3.x/pipeline_usage/OCR.html)

**Good news:** PP-OCRv5's `predict()` method in v3.x accepts **numpy arrays directly** — no file I/O needed. The PaddleOCR-VL docs confirm the `input` parameter accepts `numpy.ndarray` representing image data. Replace your pipeline step with: [paddleocr](https://www.paddleocr.ai/latest/en/version3.x/pipeline_usage/PaddleOCR-VL.html)

```python
# Pass numpy array directly — no JPEG round-trip
result = ocr.predict(warped_bgr_array)
```

If you must write to disk (e.g., for debugging), use **PNG** (`cv2.imwrite("temp.png", img)`) which is lossless. This alone may fix your ر/ن confusion.

***

## 3. Single Arabic Model vs. Dual Pass

**Drop the French model pass entirely.** Since your Arabic model (`lang='ar'`) already reads French at 0.99 confidence, the dual-pass approach adds only latency and garbage detections on Arabic zones. The `arabic_PP-OCRv5_mobile_rec` model has an 81.27% line-level accuracy on its test set — running it once and letting the LLM structure the output is the cleaner architecture. [huggingface](https://huggingface.co/PaddlePaddle/arabic_PP-OCRv5_mobile_rec/blob/main/README.md)

**On `lang='multilingual'`:** There is no generic "multilingual" mode in PP-OCRv5 for Arabic+French. The multilingual models listed (`latin_PP-OCRv5_mobile_rec`, `arabic_PP-OCRv5_mobile_rec`) are script-specific, not combined. [paddleocr](https://www.paddleocr.ai/latest/en/version3.x/pipeline_usage/OCR.html)

**On PaddleOCR-VL:** It's worth testing for your exact use case. PaddleOCR-VL accepts numpy arrays and supports Arabic numerals, but community reports indicate Arabic numeral recognition quality is still inconsistent as of late 2025. For a structured document like CNIE with known field positions, the single Arabic model + LLM is more reliable. [huggingface](https://huggingface.co/PaddlePaddle/PaddleOCR-VL/discussions/83)

***

## 4. OpenCV Preprocessing for Arabic Recognition

The order matters. Here's what actually helps PP-OCRv5's Arabic model specifically:

1. **Upscale first** (2×, `INTER_CUBIC`) — most impactful step
2. **CLAHE** on the L-channel in LAB space — boosts local contrast on ink strokes without blowing out highlights:
   ```python
   lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
   clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
   lab[:,:,0] = clahe.apply(lab[:,:,0])
   img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
   ```
3. **Unsharp mask** (not aggressive sharpening) — sharpens dot edges without amplifying JPEG artifacts:
   ```python
   blur = cv2.GaussianBlur(img, (0,0), 3)
   img = cv2.addWeighted(img, 1.5, blur, -0.5, 0)
   ```
4. **Do NOT binarize** before passing to PP-OCRv5 — the model expects BGR color input (its training pipeline uses `img_mode: BGR`) and its internal normalization handles grayscale/color conversion. Hard binarization destroys the gradient information the SVTR backbone relies on. [github](https://github.com/PaddlePaddle/PaddleOCR/issues/10358)
5. **Do NOT denoise aggressively** — bilateral or NLMeans will smooth out thin strokes that are structurally important for ر vs. ن differentiation.

**Color vs. grayscale:** Pass **color (BGR)** input. The PaddleOCR training config explicitly uses `img_mode: BGR`, and the model was trained on color data. [github](https://github.com/PaddlePaddle/PaddleOCR/issues/10358)

***

## 5. Swapping the Recognition Model

**Yes, you can fully decouple detection from recognition in PP-OCRv5.** The pipeline accepts separate `text_detection_model_name` and `text_recognition_model_name` parameters: [paddleocr](https://www.paddleocr.ai/latest/en/version3.x/pipeline_usage/OCR.html)

```python
ocr = PaddleOCR(
    text_detection_model_name="PP-OCRv5_server_det",  # keep your tuned detector
    text_recognition_model_name="arabic_PP-OCRv5_mobile_rec",  # explicit Arabic rec
    lang="ar",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
)
```

**For fixing ر/ز, غ/ع, ب/ت/ث confusion specifically**, the best path is **fine-tuning `arabic_PP-OCRv5_mobile_rec`** on CNIE-style synthetic data — because the base model's 81.27% accuracy was measured on a general Arabic benchmark, not on the specific fonts and print quality of Moroccan IDs. The confusable-character pairs you're hitting (ر/ن, غ/ع) are well-documented recognition failure modes for PP-OCR Arabic models that only targeted fine-tuning resolves. Generate 5–10k synthetic text line images from CNIE's exact font (typically a variant of Simplified Arabic) using `Pillow` + the `arabic_reshaper` + `python-bidi` libraries, and fine-tune for ~100 epochs on top of the pretrained weights. [github](https://github.com/PaddlePaddle/PaddleOCR/issues/10519)