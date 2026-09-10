from src.database import SessionLocal
from src.graph.retrieval_schemas import (
    GraphEvidenceChunk,
    GraphRelationResult,
)
from src.models.chunk import Chunk
from src.models.document import Document


def collect_source_chunk_ids(
    relationships: list[
        GraphRelationResult
    ],
) -> list[int]:
    chunk_ids = set()

    for relationship in relationships:
        for chunk_id in (
            relationship.source_chunk_ids
        ):
            chunk_ids.add(
                chunk_id
            )

    return sorted(chunk_ids)


def load_evidence_chunks(
    chunk_ids: list[int],
) -> list[GraphEvidenceChunk]:
    if not chunk_ids:
        return []

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
            .filter(
                Chunk.id.in_(
                    chunk_ids
                )
            )
            .order_by(
                Document.id,
                Chunk.chunk_index,
            )
            .all()
        )

        return [
            GraphEvidenceChunk(
                chunk_id=chunk.id,
                document_id=document.id,
                chunk_index=(
                    chunk.chunk_index
                ),
                content=chunk.content,
                source=document.source,
                title=document.title,
            )
            for chunk, document in rows
        ]


def get_graph_evidence(
    relationships: list[
        GraphRelationResult
    ],
) -> list[GraphEvidenceChunk]:
    chunk_ids = (
        collect_source_chunk_ids(
            relationships
        )
    )

    return load_evidence_chunks(
        chunk_ids
    )