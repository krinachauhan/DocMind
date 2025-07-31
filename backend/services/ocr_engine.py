from pdf2image import convert_from_path
import pytesseract
import os

IMAGE_TEMP_FOLDER = "data/images"
POPPLER_PATH = r"C:/Users/vishw/Downloads/Release-24.08.0-0/poppler-24.08.0/Library/bin"
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def run_ocr_on_pdf(pdf_path):
    os.makedirs(IMAGE_TEMP_FOLDER, exist_ok=True)
    images = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)

    full_text = ""
    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image)
        full_text += f"\n--- Page {i+1} ---\n{text.strip()}"

    return full_text.strip()

def convert_pdf_to_images(pdf_path, file_id):
    image_folder = f"data/images/{file_id}"
    os.makedirs(image_folder, exist_ok=True)
    images = convert_from_path(pdf_path)
    
    paths = []
    for i, img in enumerate(images):
        img_path = os.path.join(image_folder, f"page_{i+1}.png")
        img.save(img_path, "PNG")
        paths.append(img_path)
    return paths
