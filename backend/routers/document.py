from fastapi import APIRouter, UploadFile, File, HTTPException
from services.file_handler import save_uploaded_file
from services.pdf_utils import is_digital_pdf
from uuid import uuid4
from pydantic import BaseModel
import os
from services.smart_extractor import extract_text_smart
from pydantic import BaseModel

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