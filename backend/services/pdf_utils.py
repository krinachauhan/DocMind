import fitz  # PyMuPDF

def is_digital_pdf(pdf_path, min_text_chars=10, check_pages=3):
    """
    Returns True if the PDF contains digital text, False if it's likely scanned.
    """
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(min(check_pages, len(doc))):
            text = doc[page_num].get_text().strip()
            if len(text) >= min_text_chars:
                return True
        return False
    except Exception as e:
        print(f"Error while checking PDF: {e}")
        return False

def extract_text_directly(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text.strip()
