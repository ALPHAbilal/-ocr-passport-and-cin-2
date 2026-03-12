"""
Flask CNIE OCR + LLM Extraction API

POST /extract — accepts image, returns structured ID card fields.

Pipeline:
  1. Card detection + perspective warp (preprocessor)
  2. OCR extraction (PaddleOCR Arabic)
  3. Template text filtering (remove boilerplate)
  4. LLM field extraction (Phi-3.5-mini)
  5. City Arabic name lookup (post-correction)
"""

import time

print("[1/4] Importing libraries...")
import cv2
from flask import Flask, request, jsonify, render_template

print("[2/4] Loading preprocessor...")
from services.preprocessor import preprocess_card

print("[3/4] Loading OCR model...")
from services.ocr_engine import run_ocr

print("[4/4] Loading LLM (Phi-3.5-mini)...")
from services.llm_extractor import extract_fields
from services.template_filter import filter_detections
from services.city_lookup import fix_city_arabic

print("All models loaded!")

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
        print(f"   [{len(steps)}/5] {name} — {elapsed}ms {detail}")

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

    # --- Step 3: Template filtering ---
    raw_detections = [
        {"text": d["text"], "confidence": d["confidence"]}
        for d in ocr_result["detections"]
    ]
    filtered = filter_detections(raw_detections)
    log_step("Template filter", f"{raw_count} → {len(filtered)} useful detections")

    # --- Step 4: LLM extraction ---
    llm_result = extract_fields(filtered)
    fields = llm_result["fields"]
    log_step(
        "LLM extraction",
        f"{llm_result['time_ms']}ms | {llm_result['tokens_in']}→{llm_result['tokens_out']} tok"
    )

    if fields is None:
        log_step("LLM parse failed", llm_result["raw"][:200])
        return jsonify({
            "success": False,
            "error": "LLM failed to produce valid JSON",
            "raw_llm": llm_result["raw"],
            "steps": steps,
        }), 422

    # --- Step 5: City Arabic lookup ---
    fields = fix_city_arabic(fields)
    log_step("City lookup", f"birth_place_ar → {fields.get('birth_place_ar', 'N/A')}")

    total_ms = round((time.time() - total_start) * 1000, 1)
    print(f"   DONE in {total_ms}ms\n")

    return jsonify({
        "success": True,
        "fields": fields,
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
    app.run(host="0.0.0.0", port=5000, debug=False)
