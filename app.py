from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import base64
from pytesseract import pytesseract

pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


app = Flask(__name__)

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return thresh

def recognize_text(image):
    text = pytesseract.image_to_string(Image.fromarray(image), config='--psm 6')
    return text.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture_text', methods=['POST'])
def capture_text():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    image = Image.open(file.stream)
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    processed_image = preprocess_image(image)
    extracted_text = recognize_text(processed_image)

    return jsonify({'text': extracted_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

