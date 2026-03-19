"""
GLM-OCR CNIE — Pure OCR test. Image in, raw text out.
No field assignment, no JSON schema. Just read what's on the card.
"""

import time
from io import BytesIO

from flask import Flask, request, jsonify, render_template
from PIL import Image
from transformers import AutoProcessor, AutoModelForImageTextToText

MODEL_ID = "zai-org/GLM-OCR"

print("Loading GLM-OCR model...")
t0 = time.time()
processor = AutoProcessor.from_pretrained(MODEL_ID, trust_remote_code=True)
model = AutoModelForImageTextToText.from_pretrained(MODEL_ID, trust_remote_code=True)
model.eval()
print(f"GLM-OCR ready ({time.time() - t0:.1f}s)")

PROMPT = "Read all text visible in this image, both Arabic and French. Return every line exactly as printed."

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/extract", methods=["POST"])
def extract():
    if "image" not in request.files:
        return jsonify({"success": False, "error": "No image uploaded"}), 400

    total_start = time.time()
    image_bytes = request.files["image"].read()
    image = Image.open(BytesIO(image_bytes)).convert("RGB")

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": PROMPT},
            ],
        }
    ]

    t0 = time.time()
    inputs = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    )
    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    outputs = model.generate(**inputs, max_new_tokens=1024)
    input_len = inputs["input_ids"].shape[1]
    raw = processor.decode(outputs[0][input_len:], skip_special_tokens=True)
    elapsed_ms = (time.time() - t0) * 1000

    total_ms = round((time.time() - total_start) * 1000, 1)

    return jsonify({
        "success": True,
        "models": {
            "glm_ocr": {
                "label": "GLM-OCR (0.9B)",
                "fields": None,
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
    print("GLM-OCR — Pure OCR Test")
    print("http://localhost:5001")
    print("=" * 50)
    from werkzeug.serving import run_simple
    run_simple("0.0.0.0", 5001, app, use_reloader=False, use_debugger=False)
