# CNIE OCR — Findings So Far

## Experiment: Tesseract on Raw Phone Photo (Front Side)

### Setup
- Tesseract v5.4.0 on Windows
- Languages: eng, fra, ara
- Input: raw phone photo of front side (rotated, with table background, not cropped)

### PSM Mode Results

| PSM | Mode | Result |
|-----|------|--------|
| 3 | Automatic | Garbage — barely readable |
| 4 | Single column | Garbage — same as PSM 3 |
| 6 | Uniform block | Noisy — some fields visible but mixed with junk characters |
| 11 | Sparse text | **BEST** — found most fields correctly as separate fragments |
| 12 | Sparse text + OSD | **BEST** — same quality as PSM 11 |

### What Tesseract Successfully Read (PSM 11/12)

| Field | French | Arabic | Status |
|-------|--------|--------|--------|
| Title | ROYAUME DU MAROC | المملكة المغربية | OK |
| Card type | CARTE NATIONALE D' | البطاقة الوطنية للتعريف | OK |
| First name | BILAL | بلال | OK |
| Last name | CHAFI | شافي | OK |
| DOB | 22.01.2001 | — | OK |
| Born label | Né le | — | OK |
| Place of birth | à RABAT | — | OK |
| Gender | MI | — | OK |
| Expiry | 19.03.2029 | — | OK |
| Expiry label | Valable jusqu'au | — | OK |
| Card number | — | — | MISSED (PSM 6 read "1513538" instead of "AS13538") |

### Preprocessing Variant Results (PSM 6)

| Variant | Quality |
|---------|---------|
| Original | Best of the bunch (still noisy) |
| Grayscale | Worse — more noise |
| Otsu | Worse — lost detail |
| Adaptive | Much worse — 907 chars of garbage |
| 2x Upscale | Worse — amplified noise |
| Otsu + 2x | Worse — lost text, added artifacts |

### Key Conclusions

1. **Tesseract CAN read Arabic** — بلال (Bilal), شافي (Chafi), البطاقة الوطنية للتعريف all came through correctly
2. **PSM 11/12 (sparse text) works best on raw full photo** — but gives unstructured fragments, not field-by-field data
3. **Preprocessing HURTS on raw photos** — Otsu, adaptive threshold, upscaling all made results worse because the photo has background noise (table, shadows, card texture)
4. **Preprocessing will HELP on clean crops** — once we isolate a single field (e.g. 300x50px crop of just the name), binary threshold + upscale will remove card background texture and improve OCR
5. **Card number is problematic** — "AS13538" was read as "1513538" (letters confused with digits)
6. **We CANNOT skip the crop step** — without cropping to individual fields, we have no way to map OCR output to specific data fields

---

## Architecture Decision

### Confirmed Pipeline

```
Raw phone photo
     ↓
Step 1: FIND card in image (OpenCV contour detection)
Step 2: PERSPECTIVE CORRECT + CROP to card only
Step 3: RESIZE to 856x540
     ↓
Clean 856x540 card image
     ↓
Step 4: CROP individual field regions (using calibrated coordinates)
Step 5: PREPROCESS each crop (grayscale → otsu → upscale)
Step 6: OCR each crop with field-specific config:
        - MRZ: lang=eng, psm=6, oem=1, char whitelist
        - French names: lang=fra, psm=7
        - Arabic names: lang=ara, psm=7
        - Dates: lang=eng, psm=7
        - Card number: lang=eng, psm=8
        - Gender: lang=eng, psm=8
        - Address: lang=ara+fra, psm=6
Step 7: CROSS-VALIDATE (MRZ vs visual fields)
Step 8: OUTPUT structured JSON
```

### What Preprocessing Should Do Per Field Crop

For each small field crop (e.g. 300x50px region):
1. Convert to grayscale
2. Otsu binary threshold (removes card background texture)
3. 2x or 3x upscale (helps Tesseract with small text)
4. Pass to Tesseract with field-specific PSM + lang

This is DIFFERENT from preprocessing on the full raw photo. On a clean small crop, binary threshold removes the green card background and leaves just black text on white — exactly what Tesseract wants.

---

## Next Step: The Crop Problem

We need OpenCV to find and extract the card from the raw photo. This means:

1. Detect the card rectangle in the photo (4 corners)
2. Perspective warp to flatten any tilt/angle
3. Crop to just the card
4. Resize to 856x540

### Challenges to Think About

- **Background variation**: table color, lighting, shadows
- **Card edge detection**: the card is light green — low contrast against some backgrounds
- **Angle/tilt**: phone photos are rarely perfectly flat
- **Fingers/hands**: user might be holding the card
- **Glare**: reflective card surface can create bright spots (visible in our test image)
- **Multiple rectangles**: other objects on the table could confuse contour detection

### The Preprocessor We Built (`services/preprocessor.py`)

Already built but UNTESTED. Uses:
- Canny edge detection with multiple threshold levels
- Adaptive threshold as fallback
- Contour finding → largest quadrilateral
- Perspective warp
- Auto landscape rotation
- Resize to 856x540

Needs real-world testing with actual card photos.
