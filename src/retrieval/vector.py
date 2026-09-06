from sqlalchemy import select

from src.database import SessionLocal
from src.embeddings.service import embed_text
from src.models import Chunk, Document
from src.retrieval.schemas import RetrievedChunk


def search_similar_chunks(
    query: str,
    limit: int = 5,
) -> list[RetrievedChunk]:
    query_embedding = embed_text(query)

    distance = Chunk.embedding.cosine_distance(
        query_embedding
    )

    statement = (
        select(
            Chunk,
            Document,
            distance.label("distance"),
        )
        .join(
            Document,
            Chunk.document_id == Document.id,
        )
        .where(
            Chunk.embedding.is_not(None)
        )
        .order_by(distance)
        .limit(limit)
    )

    db = SessionLocal()

    try:
        rows = db.execute(statement).all()

        return [
            RetrievedChunk(
                chunk_id=chunk.id,
                document_id=document.id,
                chunk_index=chunk.chunk_index,
                content=chunk.content,
                source=document.source,
                title=document.title,
                distance=float(distance_value),
            )
            for chunk, document, distance_value in rows
        ]

    finally:
        db.close()