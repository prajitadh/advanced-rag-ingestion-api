import os
from datetime import datetime

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.models import Document
from app.utils.file_loader import (
    extract_text_from_pdf,
    extract_text_from_txt
)

router = APIRouter()


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Validate file type
    filename = file.filename
    file_ext = filename.split(".")[-1].lower()

    if file_ext not in ["pdf", "txt"]:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are supported"
        )

    #  Save file locally
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Extract text
    if file_ext == "pdf":
        text = extract_text_from_pdf(file_path)
        strategy = "pdf"
    else:
        text = extract_text_from_txt(file_path)
        strategy = "txt"

    # Store metadata in document DB
    document = Document(
        filename=filename,
        file_type=file_ext,
        chunking_strategy=strategy,
        uploaded_at=datetime.utcnow()
    )

    #
    db.add(document)
    db.commit()
    db.refresh(document)

    # Return response
    return {
        "message": "File uploaded successfully",
        "document_id": document.id,
        "filename": filename,
        "extracted_text_preview": text[:500]  
    }