"""
Flask CNIE OCR Comparison API

Pipeline:
  1. Card detection + perspective warp (preprocessor)
  2. Multi-OCR: PaddleOCR, DocTR, PassportEye side by side
"""

import os
import sys
import time

os.environ.setdefault("NO_COLOR", "1")

try:
    import colorama
    colorama.just_fix_windows_console()
except Exception:
    os.environ["TERM"] = "dumb"
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(errors="replace")

print("[1/3] Importing libraries...")
import cv2
from flask import Flask, request, jsonify, render_template

print("[2/3] Loading preprocessor...")
from services.preprocessor import preprocess_card

print("[3/3] Loading OCR engines...")
from services.ocr_engine import run_all_ocr

# LLM commented out for now
# from services.llm_extractor import extract_fields_all, get_loaded_models

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
        steps.append({"step": name, "elapsed_ms": elapsed, "detail": detail})
        print(f"   [{len(steps)}] {name} — {elapsed}ms {detail}")

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
        return jsonify({"success": False, "error": f"Preprocessing failed: {card_result['error']}"}), 422

    card_image = card_result["image"]
    detection = card_result["debug"].get("detection", "unknown")
    log_step("Card detection + warp", f"{detection} → {card_image.shape[1]}x{card_image.shape[0]}")

    # --- Step 2: Multi-OCR ---
    ocr_results = run_all_ocr(card_image)
    log_step("OCR engines", f"{len(ocr_results)} engines")

    # Format as model cards for frontend (same structure as LLM results)
    models = {}
    for key, result in ocr_results.items():
        dets = result["detections"]
        # Build "fields" as numbered detections for display
        fields = {}
        for i, d in enumerate(dets):
            fields[f"line_{i+1}"] = d["text"]

        models[key] = {
            "label": result["label"],
            "fields": fields if fields else None,
            "time_ms": result["time_ms"],
            "raw": "\n".join(d["text"] for d in dets) if dets else "No text detected",
            "prompt_system": None,
            "prompt_user": None,
        }

    total_ms = round((time.time() - total_start) * 1000, 1)
    print(f"   DONE in {total_ms}ms\n")

    return jsonify({
        "success": True,
        "models": models,
        "ocr_detections": [],
        "steps": steps,
        "total_ms": total_ms,
    })


if __name__ == "__main__":
    print("=" * 50)
    print("CNIE OCR Comparison")
    print("POST /extract — send image, compare OCR engines")
    print("GET  /         — web interface")
    print("http://localhost:5000")
    print("=" * 50)
    from werkzeug.serving import run_simple
    run_simple("0.0.0.0", 5000, app, use_reloader=False, use_debugger=False)
