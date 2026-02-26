"""
Flask OCR Extraction API

POST /extract — accepts image upload, runs card detection + PaddleOCR (Arabic + French).
"""

import time

print("[1/4] Importing libraries...")
import cv2
from flask import Flask, request, jsonify

print("[2/4] Loading preprocessor...")
from services.preprocessor import preprocess_card

print("[3/4] Loading OCR models (this takes a while on first run)...")
from services.ocr_engine import run_ocr
print("[4/4] All models loaded!")

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

    preprocess_mode = request.form.get("preprocess", "raw")
    if preprocess_mode not in ("raw", "upscale_2x"):
        return jsonify({
            "success": False,
            "error": f"Invalid preprocess mode '{preprocess_mode}'. Use 'raw' or 'upscale_2x'."
        }), 422

    # --- Step 1: Card detection + perspective warp (existing preprocessor) ---
    print(f"\n>> New request: file='{file.filename}', preprocess='{preprocess_mode}'")
    image_bytes = file.read()
    print(f"   [1/3] Card detection + warp... ({len(image_bytes)} bytes)")
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

    # --- Step 2: Apply preprocessing mode ---
    if preprocess_mode == "upscale_2x":
        card_image = cv2.resize(card_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        print(f"   Upscaled to {card_image.shape[1]}x{card_image.shape[0]}")

    # --- Step 3: Run OCR (both languages on full image) ---
    print("   [2/3] Running Arabic OCR...")
    ar_results = run_ocr(card_image, "ar")
    print(f"   Arabic: {ar_results['regions_found']} regions in {ar_results['time_ms']}ms")

    print("   [3/3] Running French OCR...")
    fr_results = run_ocr(card_image, "fr")
    print(f"   French: {fr_results['regions_found']} regions in {fr_results['time_ms']}ms")

    total_ms = round((time.time() - total_start) * 1000, 1)
    print(f"   DONE in {total_ms}ms")

    return jsonify({
        "arabic": [{"text": d["text"], "confidence": d["confidence"]} for d in ar_results["detections"]],
        "french": [{"text": d["text"], "confidence": d["confidence"]} for d in fr_results["detections"]],
    })


if __name__ == "__main__":
    print("=" * 50)
    print("CNIE OCR Extraction API")
    print("POST /extract — image file + preprocess param")
    print("http://localhost:5000/extract")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=False)
