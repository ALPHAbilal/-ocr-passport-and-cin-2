# Moroccan CNIE OCR Pipeline — Build Spec
## Targeting: Gen 3 (2008–2020) and Gen 4 (2020–present)

---

## Important Note on Gen 3 vs Gen 4

After research, both generations share **identical visual layout and identical MRZ format**.
The differences between them are internal only (RFID chip → NFC chip, plastic material upgrade).

**Conclusion: one single template covers both generations.**

User selection UI should therefore be:
- "My card was issued before 2020" → Gen 3
- "My card was issued after 2020" → Gen 4

Both go through the exact same extraction pipeline. No branching needed.

---

## Card Physical Specs (Both Generations)

- **Format:** ID-1 (credit card size)
- **Dimensions:** 85.6mm × 53.98mm
- **MRZ:** TD1 format — 3 lines × 30 characters (back side, bottom strip)
- **Languages:** Arabic (RTL) + French (LTR) — both on front
- **Chip:** RFID (Gen 3) / NFC contactless (Gen 4) — not used in this pipeline

---

## What the Card Contains

### Front Side — Fields

| Field | Language | Notes |
|---|---|---|
| Card number | Latin | Top-right corner, framed. Format: letter(s) + digits e.g. `AB123456` |
| Last name | Arabic + French | Both versions printed |
| First name | Arabic + French | Both versions printed |
| Date of birth | Latin numerals | Format: DD/MM/YYYY |
| Place of birth | Arabic + French | |
| Gender | Latin | M or F |
| Address | Arabic + French | Can span 2 lines |
| Expiry date | Latin numerals | Format: DD/MM/YYYY |
| Photo | — | Top-left zone |

### Back Side — Fields

| Field | Language | Notes |
|---|---|---|
| Card number | Latin | Repeated at top — use for cross-validation |
| Personal number | Latin | Unique national identifier |
| Father's name | Arabic + French | |
| Mother's name | Arabic + French | |
| MRZ Line 1 | OCR-B (Latin only) | 30 chars |
| MRZ Line 2 | OCR-B (Latin only) | 30 chars |
| MRZ Line 3 | OCR-B (Latin only) | 30 chars |

---

## Extraction Strategy

### Why MRZ first — always

The MRZ is still text on the card. OCR reads it like any other text. But it is far easier to read accurately because:
- Uses **OCR-B font** — designed specifically for optical character recognition
- **Latin characters only** — no Arabic, no mixed scripts
- **Exactly 30 chars per line** — fixed, never varies
- **High contrast zone** — no background design in that strip

This means PaddleOCR on the MRZ strip will be near 100% accurate. Everything it gives you gets used as ground truth to validate the visual OCR results.

### Full pipeline

```
User input: front image + back image
         ↓
Step 1 — NORMALIZE BOTH IMAGES
OpenCV: detect card edges → perspective correction → scale to standard size
Front: 856 × 540px
Back:  856 × 540px

         ↓
Step 2 — PROCESS BACK (MRZ first)
Crop MRZ strip (bottom 150px of back image)
Convert to grayscale + binary threshold
PaddleOCR → raw 90-character string
Regex decode → structured fields (name, DOB, card number, expiry, gender, nationality)
Check digit validation → flag any line that fails

         ↓
Step 3 — PROCESS FRONT (visual fields)
Crop each field region using fixed coordinates (see table below)
PaddleOCR on each crop individually
Post-process each field (normalize dates, strip noise chars)

         ↓
Step 4 — PROCESS BACK (non-MRZ visual fields)
Crop father name, mother name, personal number regions
PaddleOCR on each crop

         ↓
Step 5 — CROSS-VALIDATE
For each field that exists in both MRZ and visual:
  card_number, date_of_birth, expiry_date, last_name, first_name
  → MRZ value == visual value → confidence: HIGH
  → mismatch → confidence: LOW, flag field

         ↓
Step 6 — OUTPUT JSON
Merge all fields, attach confidence per field
```

---

## Normalized Dimensions & Field Coordinates

> **CRITICAL:** These coordinates are calibrated estimates based on the standard ID-1 layout.
> Developer MUST calibrate against at least 10 real card images before using in production.
> Build a visual calibration tool first: draw bounding boxes on a sample image and adjust until accurate.

### Standard normalized size: 856 × 540 px (both sides)

---

### FRONT SIDE — Field Regions

```
┌─────────────────────────────────────────────────┐  y=0
│  [HEADER: Kingdom of Morocco / Arabic title]    │  y=0–60
├──────────────┬──────────────────────────────────┤  y=60
│              │  card_number          (framed)   │  y=60–110
│    PHOTO     ├──────────────────────────────────┤  y=110
│              │  last_name_fr                    │  y=110–155
│  x:20–200    │  last_name_ar                    │  y=155–195
│  y:60–280    ├──────────────────────────────────┤  y=195
│              │  first_name_fr                   │  y=195–235
│              │  first_name_ar                   │  y=235–275
├──────────────┤  date_of_birth                   │  y=275–315
│              │  place_of_birth                  │  y=315–355
│              │  gender                          │  y=355–390
│              ├──────────────────────────────────┤  y=390
│              │  address (line 1 + 2)            │  y=390–460
│              ├──────────────────────────────────┤  y=460
│              │  expiry_date                     │  y=460–505
└─────────────────────────────────────────────────┘  y=540
```

| Field | x | y | w | h |
|---|---|---|---|---|
| card_number | 500 | 60 | 330 | 50 |
| last_name_fr | 210 | 110 | 620 | 45 |
| last_name_ar | 210 | 155 | 620 | 40 |
| first_name_fr | 210 | 195 | 620 | 40 |
| first_name_ar | 210 | 235 | 620 | 40 |
| date_of_birth | 210 | 275 | 260 | 40 |
| place_of_birth_fr | 210 | 315 | 620 | 40 |
| gender | 210 | 355 | 80 | 35 |
| address | 210 | 390 | 620 | 70 |
| expiry_date | 210 | 460 | 260 | 45 |
| photo | 20 | 60 | 180 | 220 |

---

### BACK SIDE — Field Regions

```
┌─────────────────────────────────────────────────┐  y=0
│  card_number (repeated)                         │  y=0–55
│  personal_number                                │  y=55–110
├─────────────────────────────────────────────────┤  y=110
│  father_name_fr / father_name_ar                │  y=110–190
│  mother_name_fr / mother_name_ar                │  y=190–270
├─────────────────────────────────────────────────┤  y=270
│  [barcode / chip zone — skip]                   │  y=270–390
├─────────────────────────────────────────────────┤  y=390
│  MRZ Line 1  (30 chars)                         │  y=390–438
│  MRZ Line 2  (30 chars)                         │  y=438–486
│  MRZ Line 3  (30 chars)                         │  y=486–534
└─────────────────────────────────────────────────┘  y=540
```

| Field | x | y | w | h |
|---|---|---|---|---|
| card_number_back | 20 | 0 | 400 | 55 |
| personal_number | 20 | 55 | 400 | 55 |
| father_name_fr | 20 | 110 | 816 | 40 |
| father_name_ar | 20 | 150 | 816 | 40 |
| mother_name_fr | 20 | 190 | 816 | 40 |
| mother_name_ar | 20 | 230 | 816 | 40 |
| mrz_line_1 | 0 | 390 | 856 | 48 |
| mrz_line_2 | 0 | 438 | 856 | 48 |
| mrz_line_3 | 0 | 486 | 856 | 48 |

---

## MRZ Decode Reference (TD1 — 3 lines × 30 chars)

### Line 1
```
Position  Length  Field
0–1       2       Document type → "ID" or "I<"
2–4       3       Country code  → "MAR"
5–13      9       Card number
14        1       Check digit for card number
15–29     15      Optional data (filler "<")
```

### Line 2
```
Position  Length  Field
0–5       6       Date of birth → YYMMDD
6         1       Check digit DOB
7         1       Gender → M or F
8–13      6       Expiry date → YYMMDD
14        1       Check digit expiry
15–17     3       Nationality → MAR
18–28     11      Filler "<"
29        1       Overall check digit
```

### Line 3
```
Position  Length  Field
0–29      30      Surname << Given names
                  Surname and given name separated by "<<"
                  Spaces within names replaced by "<"
```

### Check Digit Algorithm
```python
def check_digit(s: str) -> int:
    weights = [7, 3, 1]
    total = 0
    for i, c in enumerate(s):
        if c.isdigit():
            val = int(c)
        elif c.isalpha():
            val = ord(c.upper()) - 55  # A=10, B=11 ... Z=35
        else:  # '<'
            val = 0
        total += val * weights[i % 3]
    return total % 10
```

Validate: run check_digit on the field string → result must match the check digit character in the MRZ.
If it doesn't match → OCR made an error on that line → flag it, don't trust that field.

---

## MRZ OCR Preprocessing (Important)

Before passing MRZ strip to PaddleOCR:
```python
import cv2
mrz_crop = img[390:540, 0:856]          # crop MRZ zone
gray = cv2.cvtColor(mrz_crop, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# pass binary image to PaddleOCR
```
This removes any background color/texture and makes the OCR-B font trivially easy to read.

---

## Confidence Model

| Scenario | Confidence |
|---|---|
| MRZ decoded + check digit valid + matches visual OCR | `HIGH` |
| MRZ decoded + check digit valid, visual OCR not available | `HIGH` |
| MRZ decoded but check digit failed | `LOW` — flag field |
| Visual OCR only, PaddleOCR confidence > 0.85 | `MEDIUM` |
| Visual OCR only, PaddleOCR confidence < 0.85 | `LOW` — flag field |
| MRZ and visual OCR mismatch | `LOW` — flag both, return both values |

---

## Output JSON Schema

```json
{
  "status": "success",
  "generation": "gen3" | "gen4",
  "data": {
    "card_number": "AB123456",
    "last_name": "ALAOUI",
    "first_name": "YOUSSEF",
    "date_of_birth": "1990-05-14",
    "place_of_birth": "Rabat",
    "gender": "M",
    "address": "123 Rue Mohamed V, Salé",
    "expiry_date": "2030-05-14",
    "personal_number": "123456789",
    "father_name": "OMAR",
    "mother_name": "FATIMA",
    "nationality": "MAR"
  },
  "confidence": {
    "card_number": "HIGH",
    "last_name": "HIGH",
    "first_name": "HIGH",
    "date_of_birth": "HIGH",
    "expiry_date": "HIGH",
    "gender": "HIGH",
    "place_of_birth": "MEDIUM",
    "address": "MEDIUM",
    "father_name": "MEDIUM",
    "mother_name": "MEDIUM"
  }
}
```

---

## Tech Stack

| Component | Tool | Purpose |
|---|---|---|
| API | Flask | HTTP layer |
| Preprocessing | OpenCV | Perspective fix, normalize, threshold |
| OCR | PaddleOCR (CPU, `lang='arabic'`) | All text extraction |
| MRZ decode | Custom regex + check digit | Decode structured MRZ string |

### Install
```bash
pip install flask opencv-python paddlepaddle paddleocr pillow
```

---

## Project Structure

```
cnie-ocr-api/
├── app.py
├── requirements.txt
├── services/
│   ├── preprocessor.py       # OpenCV normalize + perspective correction
│   ├── ocr_engine.py         # PaddleOCR singleton (init once)
│   ├── mrz_decoder.py        # TD1 regex decode + check digit validation
│   └── field_extractor.py    # Crop regions + run OCR per field
├── templates/
│   ├── front.py              # Front field coordinates
│   └── back.py               # Back field coordinates (same for Gen3 + Gen4)
└── uploads/                  # Temp only — always deleted after processing
```

---

## API Endpoint

### `POST /api/parse-cnie`

**Request** — `multipart/form-data`

| Field | Type | Required |
|---|---|---|
| front | file (JPG/PNG) | yes |
| back | file (JPG/PNG) | yes |
| generation | string: `"gen3"` or `"gen4"` | yes |

**Example curl**
```bash
curl -X POST http://localhost:5000/api/parse-cnie \
  -F "front=@front.jpg" \
  -F "back=@back.jpg" \
  -F "generation=gen4"
```

---

## Key Implementation Rules

1. **PaddleOCR must be initialized once at startup** — never per request. It is heavy to load.
2. **Normalize before cropping** — all coordinates above assume a 856×540 normalized image. Without this step, every crop will be wrong.
3. **MRZ always processed first** — it is ground truth. Visual OCR is secondary.
4. **Apply binary threshold to MRZ crop** before OCR — see preprocessing snippet above.
5. **Always delete uploaded files** after processing — use try/finally.
6. **Calibrate coordinates with real cards** — build a simple script that draws all bounding boxes on a sample image so you can visually verify and adjust before integrating.
7. **Arabic fields** — PaddleOCR returns Arabic RTL text correctly. Do not reverse or process it. Return as-is to the client.

---

## First Build Order (Recommended)

Build in this order to de-risk early:

1. Normalization (perspective correction + scaling) — test with 5 real images
2. MRZ crop + threshold + PaddleOCR — validate check digits
3. MRZ regex decoder — get structured fields from MRZ string
4. One visual field (card_number front) — prove the crop approach works
5. All remaining visual fields
6. Cross-validation logic
7. Flask API wrapper