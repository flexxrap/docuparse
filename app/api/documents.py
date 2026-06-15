from typing import Literal

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import DocumentOut
from app.db.models import Document
from app.db.session import get_db
from app.services.ocr import extract_text
from app.services.parsers import extract_fields

router = APIRouter(prefix="/documents", tags=["documents"])

DocType = Literal["passport", "invoice", "receipt"]


@router.post("/parse", response_model=DocumentOut, status_code=201)
async def parse_document(
    file: UploadFile = File(...),
    doc_type: DocType | None = None,
    db: AsyncSession = Depends(get_db),
) -> Document:
    image_bytes = await file.read()
    raw_text = extract_text(image_bytes)
    parsed_data = extract_fields(doc_type, raw_text)

    document = Document(
        filename=file.filename,
        raw_text=raw_text,
        doc_type=doc_type,
        parsed_data=parsed_data,
    )
    db.add(document)
    await db.commit()
    await db.refresh(document)
    return document


@router.get("/{document_id}", response_model=DocumentOut)
async def get_document(document_id: int, db: AsyncSession = Depends(get_db)) -> Document:
    document = await db.get(Document, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return document
