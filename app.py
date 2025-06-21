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

# ----------- Helpers --------------------------------------------------------- #
def preprocess_image(bgr_img: np.ndarray) -> np.ndarray:
    """
    Minimal pre-processing: convert to gray and (optionally) threshold.
    Keep it lightweight; OCR still receives a 3-channel image.
    """
    gray = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)

    # # Optional extra cleaning:
    # blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # gray = cv2.threshold(blurred, 0, 255,
    #                      cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    return gray


def recognize_text(img: np.ndarray) -> str:
    """
    Run EasyOCR once per request (lazy-loaded to save cold-start RAM).
    Works on both gray or BGR images.
    """
    # Convert to RGB (EasyOCR expects RGB)
    if len(img.shape) == 2:                       # grayscale
        rgb_img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    else:                                         # BGR
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    reader = easyocr.Reader(['en'], gpu=False)    # CPU-only, single lang
    result = reader.readtext(rgb_img)
    text = " ".join([t[1] for t in result]).strip()

    # Explicit cleanup (important on small-memory dynos)
    del reader
    gc.collect()

    return text
# ----------------------------------------------------------------------------- #


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/capture_text', methods=['POST'])
def capture_text():
    try:
        if 'image' in request.files:
            img_file = request.files['image']
            print("📷 Image received via file upload")  # ✅ LOG
            img = Image.open(img_file.stream)
        else:
            data = request.get_json(force=True)
            print("📦 Received base64 payload")          # ✅ LOG
            b64 = data['image'].split(',')[1]
            img = Image.open(BytesIO(base64.b64decode(b64)))

        print(f"🖼️ Image size: {img.size}, mode: {img.mode}")  # ✅ LOG

        bgr_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        gray = preprocess_image(bgr_img)
        extracted = recognize_text(gray)

        print("📄 OCR extracted text:", extracted)  # ✅ LOG

        return jsonify({'text': extracted})

    except Exception as err:
        print(f"❌ Error during OCR: {err}")         # ✅ LOG
        return jsonify({'error': f"Internal server error: {str(err)}"}), 400


if __name__ == '__main__':
    print("✅ Flask app is starting...")  # Debug message
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
