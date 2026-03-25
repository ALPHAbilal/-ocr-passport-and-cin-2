"""
Qwen2.5-VL Arabic OCR — Single vision model, image in → structured JSON out.
Uses sherif1313/Arabic-handwritten-OCR-4bit-Qwen2.5-VL-3B-v3
(swap MODEL_ID to Misraj/Baseer when it becomes public)
"""

import json
import re
import time
from io import BytesIO

from flask import Flask, request, jsonify, render_template
from PIL import Image
import torch
from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info

MODEL_ID = "Qwen/Qwen2.5-VL-3B-Instruct"

print("Loading Qwen2.5-VL-3B-Instruct...")
t0 = time.time()

model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float32,
    device_map="cpu",
)
processor = AutoProcessor.from_pretrained(
    MODEL_ID,
    min_pixels=256 * 28 * 28,
    max_pixels=512 * 28 * 28,
)
model.eval()
print(f"Qwen2.5-VL ready ({time.time() - t0:.1f}s)")

PROMPT_STRUCTURED = """Extract fields from this Moroccan CNIE national ID card.
Return ONLY a JSON object. Copy values exactly as printed, both French and Arabic.
{"last_name_fr":"","last_name_ar":"","first_name_fr":"","first_name_ar":"","birth_date":"","birth_place_fr":"","birth_place_ar":"","card_number":"","expiry_date":"","gender":""}
null if missing."""

PROMPT_RAW = "Read all text visible in this image, both Arabic and French. Return every line exactly as printed."

app = Flask(__name__)


def _extract_json(text):
    text = text.strip().removeprefix("```json").removesuffix("```").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    matches = list(re.finditer(r'\{[^{}]*\}', text, re.DOTALL))
    for m in reversed(matches):
        try:
            return json.loads(m.group())
        except json.JSONDecodeError:
            continue
    return None


def run_ocr(pil_image, prompt, label=""):
    t = time.time()
    messages = [{
        "role": "user",
        "content": [
            {"type": "image", "image": pil_image},
            {"type": "text", "text": prompt},
        ],
    }]

    print(f"    [{label}] Building chat template...")
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    image_inputs, video_inputs = process_vision_info(messages)
    print(f"    [{label}] Processing inputs... ({time.time()-t:.1f}s)")

    inputs = processor(
        text=[text],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt",
    ).to(model.device)
    n_tokens = inputs["input_ids"].shape[1]
    print(f"    [{label}] Input: {n_tokens} tokens. Generating... ({time.time()-t:.1f}s)")

    with torch.no_grad():
        generated_ids = model.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=False,
        )

    out_tokens = generated_ids[0].shape[0] - n_tokens
    print(f"    [{label}] Generated {out_tokens} tokens ({time.time()-t:.1f}s)")

    trimmed = [out[len(inp):] for inp, out in zip(inputs.input_ids, generated_ids)]
    result = processor.batch_decode(trimmed, skip_special_tokens=True)[0]
    print(f"    [{label}] Done ({time.time()-t:.1f}s)")
    return result


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/extract", methods=["POST"])
def extract():
    if "image" not in request.files:
        return jsonify({"success": False, "error": "No image uploaded"}), 400

    total_start = time.time()
    image = Image.open(BytesIO(request.files["image"].read())).convert("RGB")

    # Run both: structured JSON + raw OCR
    models = {}

    # Structured extraction
    print(f"\n>> Structured extraction...")
    t0 = time.time()
    raw_structured = run_ocr(image, PROMPT_STRUCTURED, "Structured")
    elapsed_structured = (time.time() - t0) * 1000

    parsed = _extract_json(raw_structured)
    fields = None
    if parsed:
        fields = {k: (v if v else None) for k, v in parsed.items()}

    models["qwen_structured"] = {
        "label": "Qwen2.5-VL (Structured)",
        "fields": fields,
        "time_ms": round(elapsed_structured, 1),
        "raw": raw_structured,
        "prompt_system": None,
        "prompt_user": PROMPT_STRUCTURED,
    }

    # Raw OCR
    print(f"\n>> Raw OCR...")
    t0 = time.time()
    raw_text = run_ocr(image, PROMPT_RAW, "Raw")
    elapsed_raw = (time.time() - t0) * 1000

    # Show each line as a field
    raw_fields = {}
    for i, line in enumerate(raw_text.strip().split("\n")):
        if line.strip():
            raw_fields[f"line_{i+1}"] = line.strip()

    models["qwen_raw"] = {
        "label": "Qwen2.5-VL (Raw OCR)",
        "fields": raw_fields if raw_fields else None,
        "time_ms": round(elapsed_raw, 1),
        "raw": raw_text,
        "prompt_system": None,
        "prompt_user": PROMPT_RAW,
    }

    total_ms = round((time.time() - total_start) * 1000, 1)

    return jsonify({
        "success": True,
        "models": models,
        "ocr_detections": [],
        "total_ms": total_ms,
    })


if __name__ == "__main__":
    print("=" * 50)
    print("Qwen2.5-VL Arabic OCR Test")
    print("http://localhost:5002")
    print("=" * 50)
    from werkzeug.serving import run_simple
    run_simple("0.0.0.0", 5002, app, use_reloader=False, use_debugger=False)
