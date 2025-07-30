from services.pdf_utils import is_digital_pdf, extract_text_directly
from services.ocr_engine import run_ocr_on_pdf

def extract_text_smart(pdf_path):
    if is_digital_pdf(pdf_path):
        return {
            "file_type": "digital",
            "extracted_text": extract_text_directly(pdf_path)
        }
    else:
        return {
            "file_type": "scanned",
            "extracted_text": run_ocr_on_pdf(pdf_path)
        }
