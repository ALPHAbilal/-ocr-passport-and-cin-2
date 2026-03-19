"""
Flask CNIE OCR + LLM Extraction API

POST /extract — accepts image, returns structured ID card fields.

Pipeline:
  1. Card detection + perspective warp (preprocessor)
  2. OCR extraction (PaddleOCR Arabic)
  3. Template text filtering (remove boilerplate)
  4. Multi-model LLM extraction (Phi-3.5-mini + NuExtract-1.5)
  5. City Arabic name lookup (post-correction per model)
"""

import os
import sys
import time

os.environ.setdefault("NO_COLOR", "1")

# Fix colorama crash on Windows (OSError: Windows error 6)
try:
    import colorama
    colorama.just_fix_windows_console()
except Exception:
    os.environ["TERM"] = "dumb"
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(errors="replace")

print("[1/4] Importing libraries...")
import cv2
from flask import Flask, request, jsonify, render_template

print("[2/4] Loading preprocessor...")
from services.preprocessor import preprocess_card

print("[3/4] Loading OCR model...")
from services.ocr_engine import run_ocr

print("[4/4] Loading LLM model...")
from services.llm_extractor import extract_fields_all, get_loaded_models

print(f"All models loaded! Active: {get_loaded_models()}")

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/extract", methods=["POST"])
def extract():
    total_start = time.time()
    steps = []

    def log_step(name, detail=""):
        elapsed = round((time.time() - total_start) * 1000, 1)
        entry = {"step": name, "elapsed_ms": elapsed}
        if detail:
            entry["detail"] = detail
        steps.append(entry)
        print(f"   [{len(steps)}] {name} — {elapsed}ms {detail}")

    # --- Validate input ---
    if "image" not in request.files:
        return jsonify({"success": False, "error": "No image file provided"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"success": False, "error": "Empty filename"}), 400

    print(f"\n>> New request: file='{file.filename}'")
    image_bytes = file.read()

    # --- Step 1: Card detection + perspective warp ---
    card_result = preprocess_card(image_bytes)
    if not card_result["success"]:
        print(f"   FAILED: {card_result['error']}")
        return jsonify({
            "success": False,
            "error": f"Preprocessing failed: {card_result['error']}"
        }), 422

    card_image = card_result["image"]
    detection = card_result["debug"].get("detection", "unknown")
    log_step("Card detection + warp", f"{detection} → {card_image.shape[1]}x{card_image.shape[0]}")

    # --- Step 2: OCR extraction ---
    ocr_result = run_ocr(card_image)
    raw_count = ocr_result["regions_found"]
    log_step("OCR extraction", f"{raw_count} regions in {ocr_result['time_ms']}ms")

    # --- Step 3: LLM extraction ---
    full_detections = ocr_result["detections"]

    raw_detections = [
        {"text": d["text"], "confidence": d["confidence"]}
        for d in full_detections
    ]

    model_results = extract_fields_all(full_detections)

    for key, result in model_results.items():
        if result and result.get("fields"):
            log_step(f"LLM [{result['label']}]", f"{result['time_ms']}ms")
        elif result:
            log_step(f"LLM [{result['label']}]", f"FAILED — {result['time_ms']}ms")

    total_ms = round((time.time() - total_start) * 1000, 1)
    print(f"   DONE in {total_ms}ms\n")

    return jsonify({
        "success": True,
        "models": model_results,
        "ocr_detections": raw_detections,
        "steps": steps,
        "total_ms": total_ms,
    })


if __name__ == "__main__":
    print("=" * 50)
    print("CNIE OCR + LLM Extraction API")
    print("POST /extract — send image, get structured fields")
    print("GET  /         — web interface")
    print("http://localhost:5000")
    print("=" * 50)
    from werkzeug.serving import run_simple
    run_simple("0.0.0.0", 5000, app, use_reloader=False, use_debugger=False)
