# Tesseract Experimentation Notebook — CNIE OCR

## Goal

Run structured experiments on Tesseract to understand exactly what it can and cannot read on the CNIE card — before building any pipeline around it.

This is a discovery notebook, not production code. Every cell is an experiment. We record what works and what doesn't.

---

## Setup

```python
# Install
# pip install pytesseract opencv-python pillow pandas matplotlib

# Also install Tesseract binary + language packs:
# Ubuntu: sudo apt install tesseract-ocr tesseract-ocr-ara tesseract-ocr-fra
# Mac:    brew install tesseract
#         brew install tesseract-lang

import pytesseract
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
```

---

## Section 1 — Load & Visualize the Card

```python
# Load your card images here
front = cv2.imread("front.jpg")
back  = cv2.imread("back.jpg")

# Display both
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
axes[0].imshow(cv2.cvtColor(front, cv2.COLOR_BGR2RGB))
axes[0].set_title("Front")
axes[1].imshow(cv2.cvtColor(back, cv2.COLOR_BGR2RGB))
axes[1].set_title("Back")
plt.tight_layout()
plt.show()

# Print actual image dimensions
print(f"Front: {front.shape[1]}w × {front.shape[0]}h px")
print(f"Back:  {back.shape[1]}w × {back.shape[0]}h px")
```

---

## Section 2 — Raw Tesseract on Full Card (Baseline)

Run Tesseract with no preprocessing, no config. Just to see the baseline.

```python
def raw_tesseract(img, lang="ara+fra"):
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil = Image.fromarray(rgb)
    return pytesseract.image_to_string(pil, lang=lang)

print("=== FRONT RAW ===")
print(raw_tesseract(front))

print("\n=== BACK RAW ===")
print(raw_tesseract(back))
```

**What to record:**
- Did it read anything recognizable?
- Which fields came through correctly?
- Which were garbled?

---

## Section 3 — PSM Mode Experiments on Full Card

Tesseract has 14 page segmentation modes. Test the most relevant ones.

```python
PSM_MODES = {
    3:  "Fully automatic page segmentation (default)",
    4:  "Single column of text",
    6:  "Single uniform block of text",
    11: "Sparse text — find as much as possible",
    12: "Sparse text with OSD",
}

results = {}

for psm, description in PSM_MODES.items():
    config = f"--psm {psm}"
    text = pytesseract.image_to_string(
        Image.fromarray(cv2.cvtColor(front, cv2.COLOR_BGR2RGB)),
        lang="ara+fra",
        config=config
    )
    results[psm] = text
    print(f"\n=== PSM {psm} — {description} ===")
    print(text[:500])  # first 500 chars
```

**What to record:** which PSM gives the most structured, readable output on the full card.

---

## Section 4 — Preprocessing Variants

Test each preprocessing step in isolation to understand its effect.

```python
def show_variants(img, title=""):
    gray       = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur       = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh_otsu = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    thresh_adap = cv2.adaptiveThreshold(blur, 255,
                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                      cv2.THRESH_BINARY, 11, 2)
    upscaled   = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    variants = {
        "Original":          img,
        "Grayscale":         gray,
        "Otsu Threshold":    thresh_otsu,
        "Adaptive Threshold":thresh_adap,
        "2x Upscale":        upscaled,
    }

    fig, axes = plt.subplots(1, len(variants), figsize=(20, 4))
    for ax, (name, v) in zip(axes, variants.items()):
        if len(v.shape) == 3:
            ax.imshow(cv2.cvtColor(v, cv2.COLOR_BGR2RGB))
        else:
            ax.imshow(v, cmap='gray')
        ax.set_title(name)
        ax.axis('off')
    plt.suptitle(title)
    plt.tight_layout()
    plt.show()

    return variants

front_variants = show_variants(front, "Front Side Preprocessing Variants")
```

Now run Tesseract on each variant and compare:

```python
def ocr_all_variants(variants, lang="ara+fra", psm=6):
    config = f"--psm {psm}"
    for name, img in variants.items():
        if len(img.shape) == 3:
            pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        else:
            pil = Image.fromarray(img)
        text = pytesseract.image_to_string(pil, lang=lang, config=config)
        print(f"\n--- {name} ---")
        print(text[:300])

ocr_all_variants(front_variants)
```

**What to record:** which preprocessing + PSM combination produces the cleanest output.

---

## Section 5 — MRZ Isolation Experiment

The MRZ is the most important zone. Test it in complete isolation.

```python
def crop(img, x, y, w, h):
    return img[y:y+h, x:x+w]

# Adjust these coordinates to match your actual back image
# MRZ is always the bottom strip — measure where it starts on your image
MRZ_Y_START = int(back.shape[0] * 0.72)  # ~72% down the card
mrz_strip = back[MRZ_Y_START:, :]

# Visualize the crop
plt.figure(figsize=(14, 3))
plt.imshow(cv2.cvtColor(mrz_strip, cv2.COLOR_BGR2RGB))
plt.title("MRZ Strip Crop")
plt.axis('off')
plt.show()

# Preprocess MRZ specifically
mrz_gray = cv2.cvtColor(mrz_strip, cv2.COLOR_BGR2GRAY)
_, mrz_binary = cv2.threshold(mrz_gray, 0, 255,
                               cv2.THRESH_BINARY + cv2.THRESH_OTSU)
mrz_upscaled = cv2.resize(mrz_binary, None, fx=3, fy=3,
                           interpolation=cv2.INTER_CUBIC)

plt.figure(figsize=(14, 3))
plt.imshow(mrz_upscaled, cmap='gray')
plt.title("MRZ — Preprocessed (binary + 3x upscale)")
plt.axis('off')
plt.show()
```

Now OCR the MRZ with the config best suited for it:

```python
# MRZ = Latin only, single block, OCR-B font
# oem 1 = LSTM only (more accurate for clean text)
MRZ_CONFIG = "--psm 6 --oem 1 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789<"

mrz_text = pytesseract.image_to_string(
    Image.fromarray(mrz_upscaled),
    lang="eng",   # Latin only for MRZ — do NOT use ara+fra here
    config=MRZ_CONFIG
)

print("=== MRZ RAW OUTPUT ===")
print(mrz_text)

# Check: should be 3 lines of exactly 30 chars each
lines = [l.strip() for l in mrz_text.strip().splitlines() if l.strip()]
for i, line in enumerate(lines):
    print(f"Line {i+1}: '{line}' — length: {len(line)}")
```

**What to record:**
- Did you get 3 lines?
- Are they each 30 characters?
- Are the characters recognizable as MRZ content?

---

## Section 6 — Single Field Crop Experiments

Pick 3-4 representative fields and test cropping + OCR on each individually.

```python
# Helper: crop, display, OCR
def test_field(img, x, y, w, h, field_name, lang="ara+fra", psm=7):
    """
    PSM 7 = single text line — best for most individual fields
    PSM 8 = single word — use for short fields like gender, card number
    """
    crop_img = img[y:y+h, x:x+w]

    # Preprocess
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255,
                               cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    upscaled = cv2.resize(binary, None, fx=2, fy=2,
                           interpolation=cv2.INTER_CUBIC)

    # Display
    fig, axes = plt.subplots(1, 2, figsize=(10, 2))
    axes[0].imshow(cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB))
    axes[0].set_title(f"{field_name} — original crop")
    axes[1].imshow(upscaled, cmap='gray')
    axes[1].set_title(f"{field_name} — preprocessed")
    for ax in axes: ax.axis('off')
    plt.tight_layout()
    plt.show()

    # OCR
    config = f"--psm {psm}"
    result = pytesseract.image_to_string(
        Image.fromarray(upscaled), lang=lang, config=config
    ).strip()

    print(f"Field: {field_name}")
    print(f"Result: '{result}'")
    print(f"PSM: {psm} | Lang: {lang}")
    print("---")
    return result
```

Run on key fields — adjust coordinates to match your card:

```python
# These are starting estimates — measure on your actual image
results = {}

results["card_number"]   = test_field(front, x=500, y=60,  w=330, h=50,  field_name="card_number",   lang="eng", psm=8)
results["last_name_fr"]  = test_field(front, x=210, y=110, w=620, h=45,  field_name="last_name_fr",  lang="fra", psm=7)
results["last_name_ar"]  = test_field(front, x=210, y=155, w=620, h=40,  field_name="last_name_ar",  lang="ara", psm=7)
results["date_of_birth"] = test_field(front, x=210, y=275, w=260, h=40,  field_name="date_of_birth", lang="eng", psm=7)
results["address"]       = test_field(front, x=210, y=390, w=620, h=70,  field_name="address",       lang="ara+fra", psm=6)

print("\n=== SUMMARY ===")
for field, value in results.items():
    print(f"{field:20s} → '{value}'")
```

---

## Section 7 — Language Pack Comparison

Test Arabic-only vs French-only vs combined on the same field.

```python
def compare_languages(img, x, y, w, h, field_name, psm=7):
    crop_img = img[y:y+h, x:x+w]
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    upscaled = cv2.resize(binary, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    pil = Image.fromarray(upscaled)
    config = f"--psm {psm}"

    langs = ["ara", "fra", "ara+fra", "eng"]
    print(f"\n=== Language comparison: {field_name} ===")
    for lang in langs:
        result = pytesseract.image_to_string(pil, lang=lang, config=config).strip()
        print(f"  {lang:10s} → '{result}'")

# Test on last name (has both Arabic and French versions)
compare_languages(front, x=210, y=110, w=620, h=45, field_name="last_name_fr_zone")
compare_languages(front, x=210, y=155, w=620, h=40, field_name="last_name_ar_zone")
```

---

## Section 8 — Results Table

Record everything in a structured table for comparison.

```python
# Fill this in as you run experiments
experiment_log = [
    # {
    #   "field": "last_name_fr",
    #   "preprocessing": "grayscale + otsu + 2x upscale",
    #   "psm": 7,
    #   "lang": "fra",
    #   "output": "ALAOUI",
    #   "correct": True,
    #   "notes": ""
    # },
]

df = pd.DataFrame(experiment_log)
if not df.empty:
    print(df.to_string())
```

---

## Section 9 — What to Look For

After running all experiments, answer these questions:

**MRZ:**
- [ ] Did Tesseract read all 3 lines?
- [ ] Were lines exactly 30 characters?
- [ ] Were card number, DOB, expiry readable?

**Visual fields (French):**
- [ ] Last name readable?
- [ ] First name readable?
- [ ] Date of birth readable?
- [ ] Address readable?

**Visual fields (Arabic):**
- [ ] Any Arabic text readable at all?
- [ ] Better with `ara` alone or `ara+fra` combined?

**Preprocessing:**
- [ ] Which preprocessing worked best: raw / grayscale / otsu / adaptive?
- [ ] Did upscaling help or hurt?

**PSM:**
- [ ] Which PSM worked best for single-line fields?
- [ ] Which PSM worked best for multi-line fields (address)?

---

## Section 10 — Quick MRZ Decoder (Bonus)

If MRZ reads correctly, decode it here to validate.

```python
def decode_mrz(mrz_text):
    lines = [l.strip() for l in mrz_text.strip().splitlines() if l.strip()]
    if len(lines) < 3:
        print(f"ERROR: Expected 3 lines, got {len(lines)}")
        return None

    l1, l2, l3 = lines[0], lines[1], lines[2]
    print(f"Line 1 ({len(l1)} chars): {l1}")
    print(f"Line 2 ({len(l2)} chars): {l2}")
    print(f"Line 3 ({len(l3)} chars): {l3}")

    if len(l1) < 30 or len(l2) < 30 or len(l3) < 30:
        print("WARNING: Lines shorter than 30 chars — OCR likely missed characters")

    result = {
        "doc_type":    l1[0:2].replace("<", "").strip(),
        "country":     l1[2:5].replace("<", "").strip(),
        "card_number": l1[5:14].replace("<", "").strip(),
        "dob":         l2[0:6],   # YYMMDD
        "gender":      l2[7],
        "expiry":      l2[8:14],  # YYMMDD
        "nationality": l2[15:18].replace("<", "").strip(),
        "full_name":   l3.replace("<", " ").strip(),
    }

    # Parse name
    if "  " in result["full_name"]:
        parts = result["full_name"].split("  ")
        result["last_name"]  = parts[0].strip()
        result["first_name"] = parts[1].strip() if len(parts) > 1 else ""

    # Parse dates
    def parse_date(yymmdd):
        try:
            yy, mm, dd = yymmdd[:2], yymmdd[2:4], yymmdd[4:6]
            year = f"19{yy}" if int(yy) > 30 else f"20{yy}"
            return f"{year}-{mm}-{dd}"
        except:
            return yymmdd

    result["dob_parsed"]    = parse_date(result["dob"])
    result["expiry_parsed"] = parse_date(result["expiry"])

    return result

decoded = decode_mrz(mrz_text)
if decoded:
    for k, v in decoded.items():
        print(f"  {k:15s}: {v}")
```

---

## What to Report Back

After running the notebook, come back with:

1. **MRZ result** — did it work? How many chars per line?
2. **Best preprocessing combo** — which variant gave cleanest text?
3. **Best PSM per field type** — single line vs block
4. **Arabic quality** — readable or garbage?
5. **Biggest failure point** — which field is hardest?

That information will tell us exactly how to design the real pipeline.