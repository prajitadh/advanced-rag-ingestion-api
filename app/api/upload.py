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

from app.services.chunking import chunk_text
from app.services.embeddings import get_embeddings
from app.vectorstore.qdrant_client import create_collection, upsert_chunks

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

    # Save file
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Extract text
    if file_ext == "pdf":
        text = extract_text_from_pdf(file_path)
    else:
        text = extract_text_from_txt(file_path)

    # Ensure file isn't empty
    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="No text could be extracted from the file."
        )

    # Chunk text
    chunks = chunk_text(text, strategy="recursive")

    # Save document metadata
    document = Document(
        filename=filename,
        file_type=file_ext,
        chunking_strategy="recursive",
        uploaded_at=datetime.utcnow()
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    # Generate embeddings
    embeddings = get_embeddings(chunks)

    # Create Qdrant collection if it doesn't exist
    create_collection()

    # Store vectors
    upsert_chunks(
        chunks=chunks,
        embeddings=embeddings,
        document_id=document.id
    )

    return {
        "message": "File uploaded successfully",
        "document_id": document.id,
        "filename": filename,
        "chunks_created": len(chunks),
        "preview": text[:300]
    }