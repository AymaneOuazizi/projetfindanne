import hashlib

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models import Chunk, Document


def calculate_content_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def split_text(
    content: str,
    chunk_size: int = 500,
) -> list[str]:
    chunks = []

    for start in range(0, len(content), chunk_size):
        chunk = content[start : start + chunk_size]
        chunks.append(chunk)

    return chunks


def ingest_document(
    db: Session,
    title: str,
    source: str,
    content: str,
    language: str = "en",
) -> Document:
    content_hash = calculate_content_hash(content)

    existing_document = db.scalar(
        select(Document).where(
            Document.content_hash == content_hash
        )
    )

    if existing_document:
        return existing_document

    document = Document(
        title=title,
        source=source,
        language=language,
        content_hash=content_hash,
    )

    db.add(document)
    db.flush()

    chunks = split_text(content)

    for index, chunk_content in enumerate(chunks):
        chunk = Chunk(
            document_id=document.id,
            chunk_index=index,
            content=chunk_content,
        )

        db.add(chunk)

    db.commit()
    db.refresh(document)

    return document