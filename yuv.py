

import cv2
from PIL import Image 
from pytesseract import pytesseract

# Set the path to the Tesseract executable
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return thresh

def recognize_text(image):
    text = pytesseract.image_to_string(Image.fromarray(image), config='--psm 6')
    print("Recognized Text:", text[:-1])

    # Draw the recognized text on the image
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (50, 50)
    fontScale = 1
    color = (255, 0, 0)
    thickness = 2
    cv2.putText(image, text[:-1], org, font, fontScale, color, thickness, cv2.LINE_AA)

# Open the camera
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    # Capture frame-by-frame
    _, image = camera.read()

    # Preprocess the image
    preprocessed_image = preprocess_image(image)

    # Display the preprocessed image
    cv2.imshow('Text detection', preprocessed_image)

    # Press 's' to capture the image and recognize text
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite('captured_image.jpg', preprocessed_image)
        recognize_text(preprocessed_image)
        cv2.imshow('Text detection', preprocessed_image) # Show the image with recognized text

    # Press 'q' to quit
    elif cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
camera.release()
cv2.destroyAllWindows()
