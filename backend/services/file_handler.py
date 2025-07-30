import os
import shutil
from fastapi import UploadFile

UPLOAD_FOLDER = "data/uploads"

def save_uploaded_file(file: UploadFile, file_id: str) -> str:

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    ext = file.filename.split(".")[-1]
    file_name = f"{file_id}.{ext}"

    file_path = os.path.join(UPLOAD_FOLDER, file_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path    

