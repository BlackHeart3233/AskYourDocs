"""
Created script where u can insert pdf, jpg or png file and it will extract text from it using OCR.

"""
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_pil(img):
    #PIL -> OpenCV
    img = np.array(img)
    #grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #resize (beter OCR)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    #threshold (contrast)
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
    return thresh


def ocr_image(img):
    processed = preprocess_pil(img)
    return pytesseract.image_to_string(
        processed,
        lang="slv+eng",
        config="--psm 6" //treba pregleda za različne tipe dokumentov
    )


def extract_text(file):
    ext = os.path.splitext(file)[1].lower()
    if ext in [".jpg", ".png"]:
        img = Image.open(file)
        return ocr_image(img)
    elif ext == ".pdf":
        pages = convert_from_path(file, dpi=200, poppler_path=r"C:\poppler\Library\bin")
        text = ""
        for p in pages:
            text += ocr_image(p)
        return text
    else:
        return "Unsupported file"


print(extract_text("test.pdf"))