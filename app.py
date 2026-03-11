"""
Flask OCR Extraction API

POST /extract — accepts image upload, runs card detection + single-pass OCR.
"""

import time

print("[1/3] Importing libraries...")
import cv2
from flask import Flask, request, jsonify

print("[2/3] Loading preprocessor...")
from services.preprocessor import preprocess_card

print("[3/3] Loading OCR model (this takes a while on first run)...")
from services.ocr_engine import run_ocr
print("All models loaded!")

app = Flask(__name__)


@app.route("/extract", methods=["POST"])
def extract():
    total_start = time.time()

    # --- Validate input ---
    if "image" not in request.files:
        return jsonify({"success": False, "error": "No image file provided"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"success": False, "error": "Empty filename"}), 400

    # --- Step 1: Card detection + perspective warp ---
    print(f"\n>> New request: file='{file.filename}'")
    image_bytes = file.read()
    print(f"   [1/2] Card detection + warp... ({len(image_bytes)} bytes)")
    card_result = preprocess_card(image_bytes)

    if not card_result["success"]:
        print(f"   FAILED: {card_result['error']}")
        return jsonify({
            "success": False,
            "error": f"Preprocessing failed: {card_result['error']}"
        }), 422

    card_image = card_result["image"]  # numpy array, 856x540 BGR
    card_debug = card_result["debug"]
    print(f"   Card: {card_debug.get('detection', '?')} -> {card_image.shape[1]}x{card_image.shape[0]}")

    # --- Step 2: Single-pass OCR (Arabic model reads both scripts) ---
    # Enhancement (2x upscale, CLAHE, unsharp mask) happens inside run_ocr
    print("   [2/2] Running OCR (single pass, enhanced)...")
    results = run_ocr(card_image)
    print(f"   OCR: {results['regions_found']} regions in {results['time_ms']}ms")

    total_ms = round((time.time() - total_start) * 1000, 1)
    print(f"   DONE in {total_ms}ms")

    return jsonify({
        "detections": [
            {"text": d["text"], "confidence": d["confidence"]}
            for d in results["detections"]
        ],
    })


if __name__ == "__main__":
    print("=" * 50)
    print("CNIE OCR Extraction API")
    print("POST /extract — send image, get OCR text")
    print("http://localhost:5000/extract")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=False)
