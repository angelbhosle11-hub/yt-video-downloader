from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # frontend se requests allow karne ke liye

SAVE_DIR = "captured_frames"
os.makedirs(SAVE_DIR, exist_ok=True)

@app.route('/upload', methods=['POST', 'OPTIONS'])
def upload_frame():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({"error": "No image data"}), 400

    image_data = data['image'].split(',')[1]
    img_bytes = base64.b64decode(image_data)
    np_arr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = os.path.join(SAVE_DIR, f"frame_{timestamp}.jpg")
    cv2.imwrite(filename, frame)

    return jsonify({"status": "saved", "file": filename}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render 5000 use karta hai
    app.run(host="0.0.0.0", port=port, debug=False)
