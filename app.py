from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import base64
import easyocr
import gc  # for memory cleanup

app = Flask(__name__)

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Optional: Apply thresholding for better results
    # blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return gray

def recognize_text(image):
    # Initialize EasyOCR reader inside the function to save memory
    reader = easyocr.Reader(['en'], gpu=False)  # GPU off for most hosting platforms
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = reader.readtext(rgb_image)
    extracted_text = " ".join([text[1] for text in result])

    # Clean up memory
    del reader
    gc.collect()

    return extracted_text.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture_text', methods=['POST'])
def capture_text():
    try:
        if 'image' in request.files:
            file = request.files['image']
            image = Image.open(file.stream)
        else:
            data = request.get_json()
            base64_image = data['image'].split(',')[1]
            image_data = base64.b64decode(base64_image)
            image = Image.open(BytesIO(image_data))

        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        processed_image = preprocess_image(image)
        extracted_text = recognize_text(processed_image)

        return jsonify({'text': extracted_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 8080))  # Railway uses PORT env
    app.run(host='0.0.0.0', port=port)
