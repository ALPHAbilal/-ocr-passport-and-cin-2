"""
Gemma 3 4B Vision — CNIE extraction test.
Image in → structured JSON out. Supports Arabic + French.
"""

import json
import re
import time
from io import BytesIO

from flask import Flask, request, jsonify, render_template
from PIL import Image
import torch
from transformers import Gemma3ForConditionalGeneration, AutoProcessor

MODEL_ID = "google/gemma-3-4b-it"

print("Loading Gemma 3 4B...")
t0 = time.time()
model = Gemma3ForConditionalGeneration.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.bfloat16,
    device_map="cpu",
)
processor = AutoProcessor.from_pretrained(MODEL_ID)
model.eval()
print(f"Gemma 3 4B ready ({time.time() - t0:.1f}s)")

PROMPT = """Extract fields from this Moroccan CNIE national ID card.
Return ONLY a JSON object. Read both French and Arabic text on the card.
{"last_name_fr":"","last_name_ar":"","first_name_fr":"","first_name_ar":"","birth_date":"","birth_place_fr":"","birth_place_ar":"","card_number":"","expiry_date":"","gender":""}
- birth_place_fr: the CITY name only, strip "a " or "à " prefix
- birth_place_ar: the Arabic CITY name only (e.g. الرباط), not the label "مزداد بتاريخ"
- gender: look for single letter M or F on the card
- null if missing"""

app = Flask(__name__)


def _extract_json(text):
    cleaned = text.strip().removeprefix("```json").removesuffix("```").strip()
    try:
        return json.loads(cleaned)
    except (json.JSONDecodeError, TypeError):
        pass
    matches = list(re.finditer(r'\{[^{}]*\}', text, re.DOTALL))
    for m in reversed(matches):
        try:
            return json.loads(m.group())
        except json.JSONDecodeError:
            continue
    return None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/extract", methods=["POST"])
def extract():
    if "image" not in request.files:
        return jsonify({"success": False, "error": "No image uploaded"}), 400

    total_start = time.time()
    image = Image.open(BytesIO(request.files["image"].read())).convert("RGB")
    print(f"\n>> Image: {image.size[0]}x{image.size[1]}")

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": PROMPT},
            ],
        }
    ]

    print("  Processing inputs...")
    t0 = time.time()
    inputs = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    ).to(model.device)
    n_tokens = inputs["input_ids"].shape[1]
    print(f"  Input: {n_tokens} tokens ({time.time() - t0:.1f}s)")

    print("  Generating...")
    t_gen = time.time()
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=300, do_sample=False)
    out_tokens = outputs[0].shape[0] - n_tokens
    print(f"  Generated {out_tokens} tokens ({time.time() - t_gen:.1f}s)")

    raw = processor.decode(outputs[0][n_tokens:], skip_special_tokens=True)
    elapsed_ms = (time.time() - t0) * 1000
    total_ms = round((time.time() - total_start) * 1000, 1)

    print(f"  Output: {raw[:200]}...")
    print(f"  Total: {total_ms}ms")

    # Parse JSON
    parsed = _extract_json(raw)
    fields = None
    if parsed:
        fields = {k: (v if v else None) for k, v in parsed.items()}

    return jsonify({
        "success": True,
        "models": {
            "gemma3": {
                "label": "Gemma 3 4B",
                "fields": fields,
                "time_ms": round(elapsed_ms, 1),
                "raw": raw,
                "prompt_system": None,
                "prompt_user": PROMPT,
            }
        },
        "ocr_detections": [],
        "total_ms": total_ms,
    })


if __name__ == "__main__":
    print("=" * 50)
    print("Gemma 3 4B — CNIE Extraction Test")
    print("http://localhost:5003")
    print("=" * 50)
    from werkzeug.serving import run_simple
    run_simple("0.0.0.0", 5003, app, use_reloader=False, use_debugger=False)
