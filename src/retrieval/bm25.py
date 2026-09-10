from rank_bm25 import BM25Okapi

from src.database import SessionLocal
from src.models.chunk import Chunk
from src.models.document import Document
from src.retrieval.schemas import (
    BM25RetrievedChunk,
)
from src.retrieval.tokenizer import tokenize


def search_bm25_chunks(
    query: str,
    limit: int = 5,
) -> list[BM25RetrievedChunk]:
    with SessionLocal() as session:
        rows = (
            session.query(
                Chunk,
                Document,
            )
            .join(
                Document,
                Chunk.document_id
                == Document.id,
            )
            .all()
        )

        if not rows:
            return []

        tokenized_corpus = [
            tokenize(chunk.content)
            for chunk, _ in rows
        ]

        bm25 = BM25Okapi(
            tokenized_corpus
        )

        tokenized_query = tokenize(
            query
        )

        scores = bm25.get_scores(
            tokenized_query
        )

        scored_rows = []

        for (
            (chunk, document),
            score,
        ) in zip(
            rows,
            scores,
        ):
            scored_rows.append(
                (
                    chunk,
                    document,
                    float(score),
                )
            )

        scored_rows.sort(
            key=lambda item: item[2],
            reverse=True,
        )

        top_rows = scored_rows[:limit]

        return [
            BM25RetrievedChunk(
                chunk_id=chunk.id,
                document_id=document.id,
                chunk_index=chunk.chunk_index,
                content=chunk.content,
                source=document.source,
                title=document.title,
                score=score,
            )
            for (
                chunk,
                document,
                score,
            ) in top_rows
        ]