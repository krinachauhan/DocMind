from pdf2image import convert_from_path
import pytesseract
import os

IMAGE_TEMP_FOLDER = "data/images"

def run_ocr_on_pdf(pdf_path):
    os.makedirs(IMAGE_TEMP_FOLDER, exist_ok=True)
    images = convert_from_path(pdf_path)

    full_text = ""
    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image)
        full_text += f"\n--- Page {i+1} ---\n{text.strip()}"

    return full_text.strip()
