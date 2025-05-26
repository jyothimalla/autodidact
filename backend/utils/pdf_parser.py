import fitz  # PyMuPDF
from pdf2image import convert_from_path
import pytesseract
import cv2
import os
import tempfile
from PIL import Image
import re
import numpy as np
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def extract_answers_from_pdf(pdf_path):
    answers = []

    with tempfile.TemporaryDirectory() as path:
        # Convert PDF pages to images
        pages = convert_from_path(pdf_path, dpi=300, output_folder=path)
        
        for page_num, page_image in enumerate(pages):
            # Convert PIL image to OpenCV format
            open_cv_image = cv2.cvtColor(np.array(page_image), cv2.COLOR_RGB2BGR)

            # Optional: Preprocess image (blur, threshold etc.)
            gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

            # OCR to extract text
            text = pytesseract.image_to_string(gray)

            # Extract pattern like: "Q1: Answer", "1. Answer", etc.
            matches = re.findall(r'(?:Q|q)?\s?(\d+)[\:\.\-]?\s*([A-Ea-e])', text)
            for qno, ans in matches:
                answers.append({
                    'question_number': int(qno),
                    'answer': ans.upper()
                })

    return answers