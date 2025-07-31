from fastapi import APIRouter, UploadFile, File, HTTPException
from services.file_handler import save_uploaded_file
from services.pdf_utils import is_digital_pdf
from uuid import uuid4
from pydantic import BaseModel
import os
from services.smart_extractor import extract_text_smart
from pydantic import BaseModel
from services.text_saver import save_text_to_file
from services.ocr_engine import convert_pdf_to_images

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    # Validate file type
    allowed_types = ["application/pdf", "image/png", "image/jpeg", "image/jpg"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type. Upload PDF or image only.")
    
    # Save file
    file_id = str(uuid4())
    file_path = save_uploaded_file(file, file_id)

    return {
        "file_id": file_id,
        "file_name": file.filename,
        "file_path": file_path
    }

class FilePathRequest(BaseModel):
    file_path: str

@router.post("/check_type")
def check_pdf_type(request: FilePathRequest):
    file_path = request.file_path

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    if not file_path.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported for this check.")

    is_digital = is_digital_pdf(file_path)

    return {
        "file_type": "digital" if is_digital else "scanned",
        "file_path": file_path
    }

class ExtractTextRequest(BaseModel):
    file_path: str

@router.post("/extract_text")
def extract_text(request: ExtractTextRequest):
    if not os.path.exists(request.file_path):
        raise HTTPException(status_code=404, detail="File not found")

    result = extract_text_smart(request.file_path)
    return result


@router.post("/process_document")
async def process_document(file: UploadFile = File(...)):
    # Validate file
    allowed_types = ["application/pdf", "image/jpeg", "image/png"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type.")
    
    # Save original file
    file_id = str(uuid4())
    file_path = save_uploaded_file(file, file_id)

    # Smart extract (checks type and extracts text)
    result = extract_text_smart(file_path)
    text = result["extracted_text"]
    if not text:
        raise HTTPException(status_code=500, detail="Text extraction failed. Please check the document format.")

    file_type = result["file_type"]

    base_folder = os.path.join("data", "text")
    text_path = os.path.join(base_folder, f"{file_id}.txt")
    # Save extracted text as .txt
    with open(text_path, "a", encoding="utf-8") as f:
        f.write(text + "\n")

    return {
        "file_id": file_id,
        "file_type": file_type,
        "text_file_path": text_path,
        "preview": text[:300]  # optional preview
    }