from sqlalchemy import select

from src.database import SessionLocal
from src.embeddings.service import embed_texts
from src.models import Chunk


def generate_missing_embeddings() -> int:
    db = SessionLocal()

    try:
        chunks = db.scalars(
            select(Chunk).where(Chunk.embedding.is_(None))
        ).all()

        if not chunks:
            return 0

        texts = [chunk.content for chunk in chunks]

        embeddings = embed_texts(texts)

        for chunk, embedding in zip(
            chunks,
            embeddings,
            strict=True,
        ):
            chunk.embedding = embedding

        db.commit()

        return len(chunks)

    finally:
        db.close()