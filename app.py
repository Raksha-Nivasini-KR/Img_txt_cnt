from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import base64
from pytesseract import pytesseract

# Set the path to the Tesseract executable
pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = Flask(__name__)  # Corrected this line

def preprocess_image(image):
    """ Convert image to grayscale, blur, and apply thresholding """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return thresh

def recognize_text(image):
    """ Extract text from the processed image using Tesseract OCR """
    text = pytesseract.image_to_string(Image.fromarray(image), config='--psm 6')
    return text.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture_text', methods=['POST'])
def capture_text():
    if 'image' in request.files:
        file = request.files['image']
        image = Image.open(file)
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    elif request.json and 'image' in request.json:
        image_data = request.json['image']
        image_data = base64.b64decode(image_data.split(',')[1])  # Decode Base64
        image = Image.open(BytesIO(image_data))
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    else:
        return jsonify({'error': 'No image provided'}), 400

    processed_image = preprocess_image(image)
    extracted_text = recognize_text(processed_image)

    return jsonify({'text': extracted_text})

if __name__ == '__main__':  # Corrected this line
    app.run(debug=True)
