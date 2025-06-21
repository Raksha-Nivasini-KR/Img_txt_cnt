# app.py
from flask import Flask, request, jsonify, render_template
import cv2                      # use opencv-python-headless in requirements
import numpy as np
from PIL import Image
from io import BytesIO
import base64
import easyocr
import gc                       # for memory cleanup
import os

app = Flask(__name__)

# ✅ Preload the EasyOCR model (before the first request)
print("📦 Preloading EasyOCR model...")
reader = easyocr.Reader(['en'], gpu=False)
print("✅ EasyOCR model loaded.")

# ----------- Helpers --------------------------------------------------------- #
def preprocess_image(bgr_img: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
    return gray

def recognize_text(img: np.ndarray) -> str:
    rgb_img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB) if len(img.shape) == 2 else cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = reader.readtext(rgb_img, detail=0, paragraph=True)
    text = " ".join(result).strip()
    gc.collect()
    return text
# ----------------------------------------------------------------------------- #

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture_text', methods=['POST'])
def capture_text():
    try:
        # --- Step 1: Load the image from file or base64 ---
        if 'image' in request.files:
            img_file = request.files['image']
            print("📷 Image received via file upload")
            img = Image.open(img_file.stream)
        else:
            data = request.get_json(force=True)
            print("📦 Received base64 payload")
            b64 = data['image'].split(',')[1]
            img = Image.open(BytesIO(base64.b64decode(b64)))

        img = img.convert("RGB")
        print(f"🖼️ Original image size: {img.size}, mode: {img.mode}")

        # --- Step 2: Resize if the image is too large ---
        MAX_DIM = 1024
        if max(img.size) > MAX_DIM:
            img.thumbnail((MAX_DIM, MAX_DIM), Image.LANCZOS)
            print(f"🔄 Resized image to: {img.size}")

        # --- Step 3: Convert to OpenCV format ---
        bgr_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        # --- Step 4: OCR Pipeline ---
        gray = preprocess_image(bgr_img)
        extracted = recognize_text(gray)

        print("📄 OCR extracted text:", extracted)
        return jsonify({'text': extracted})

    except Exception as err:
        print(f"❌ Error during OCR: {err}")
        return jsonify({'error': f"Internal server error: {str(err)}"}), 400

if __name__ == '__main__':
    print("✅ Flask app is starting...")
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
