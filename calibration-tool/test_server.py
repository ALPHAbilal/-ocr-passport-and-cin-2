"""
Test server for the calibration tool.
Serves the HTML page + provides a /preprocess endpoint.

Usage:
    pip install flask opencv-python numpy
    python test_server.py
    Open http://localhost:5050
"""

import sys
import os

# add parent dir so we can import services
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify, send_from_directory, Response
import cv2
import numpy as np
from services.preprocessor import preprocess_card

app = Flask(__name__)

# serve the HTML page
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

# preprocess endpoint: accepts raw image, returns cleaned 856x540 card
@app.route("/preprocess", methods=["POST"])
def preprocess():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files["image"]
    image_bytes = file.read()

    result = preprocess_card(image_bytes)

    if not result["success"]:
        return jsonify({"error": result["error"], "debug": result["debug"]}), 422

    # encode processed image as JPEG and return it
    _, buffer = cv2.imencode(".jpg", result["image"], [cv2.IMWRITE_JPEG_QUALITY, 95])

    return Response(
        buffer.tobytes(),
        mimetype="image/jpeg",
        headers={
            "X-Debug-Info": str(result["debug"]),
            "X-Detection": result["debug"].get("detection", "unknown"),
        }
    )


if __name__ == "__main__":
    print("=" * 50)
    print("CNIE Calibration Tool - Test Server")
    print("Open http://localhost:5050")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5050, debug=True)
