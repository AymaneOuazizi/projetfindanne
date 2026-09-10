from datetime import datetime, timezone

from sqlalchemy import select

from src.database import SessionLocal
from src.graph.pipeline import (
    run_graph_extraction_pipeline,
)
from src.graph.sync import (
    sync_postgres_to_neo4j,
)
from src.models.chunk import Chunk


def load_pending_graph_chunks() -> list[dict]:
    """
    Load chunks that have not yet been successfully
    processed by the GraphRAG extraction pipeline.
    """

    with SessionLocal() as session:
        chunks = session.scalars(
            select(Chunk)
            .where(
                Chunk.graph_processed.is_(False)
            )
            .order_by(
                Chunk.document_id,
                Chunk.chunk_index,
            )
        ).all()

        return [
            {
                "chunk_id": chunk.id,
                "document_id": (
                    chunk.document_id
                ),
            }
            for chunk in chunks
        ]


def mark_chunks_as_graph_processed(
    chunk_ids: list[int],
) -> int:
    """
    Mark successfully extracted chunks as processed.

    Failed chunks are intentionally not included so
    they can be retried later.
    """

    if not chunk_ids:
        return 0

    processed_at = datetime.now(
        timezone.utc
    )

    with SessionLocal() as session:
        chunks = session.scalars(
            select(Chunk).where(
                Chunk.id.in_(chunk_ids)
            )
        ).all()

        for chunk in chunks:
            chunk.graph_processed = True
            chunk.graph_processed_at = (
                processed_at
            )

        session.commit()

        return len(chunks)


def sync_knowledge_graph_incrementally() -> dict:
    """
    Incrementally synchronize PostgreSQL content with
    Neo4j and extract graph knowledge only from chunks
    that have not already been processed.
    """

    pending_chunks = (
        load_pending_graph_chunks()
    )

    if not pending_chunks:
        return {
            "pending_chunks": 0,
            "documents_synced": 0,
            "chunks_synced": 0,
            "chunks_processed": 0,
            "chunks_failed": 0,
            "entities_extracted": 0,
            "relationships_extracted": 0,
            "chunks_marked_processed": 0,
        }

    chunk_ids = [
        item["chunk_id"]
        for item in pending_chunks
    ]

    document_ids = sorted(
        {
            item["document_id"]
            for item in pending_chunks
        }
    )

    print(
        f"Found {len(chunk_ids)} "
        "pending graph chunks."
    )

    print(
        "1. Synchronizing new documents "
        "and chunks to Neo4j..."
    )

    sync_result = (
        sync_postgres_to_neo4j(
            document_ids=document_ids,
            chunk_ids=chunk_ids,
        )
    )

    print(
        "2. Extracting graph knowledge "
        "from pending chunks..."
    )

    extraction_result = (
        run_graph_extraction_pipeline(
            chunk_ids=chunk_ids
        )
    )

    successful_chunk_ids = [
        result["chunk_id"]
        for result
        in extraction_result["results"]
        if result["status"] == "success"
    ]

    failed_chunk_ids = [
        result["chunk_id"]
        for result
        in extraction_result["results"]
        if result["status"] == "failed"
    ]

    print(
        "3. Marking successful chunks "
        "as processed..."
    )

    marked_count = (
        mark_chunks_as_graph_processed(
            successful_chunk_ids
        )
    )

    if failed_chunk_ids:
        print(
            "Chunks remaining for retry: "
            f"{failed_chunk_ids}"
        )

    return {
        "pending_chunks": len(
            chunk_ids
        ),
        "documents_synced": (
            sync_result["documents"]
        ),
        "chunks_synced": (
            sync_result["chunks"]
        ),
        "chunks_processed": (
            extraction_result[
                "chunks_processed"
            ]
        ),
        "chunks_failed": (
            extraction_result[
                "chunks_failed"
            ]
        ),
        "entities_extracted": (
            extraction_result[
                "entities_extracted"
            ]
        ),
        "relationships_extracted": (
            extraction_result[
                "relationships_extracted"
            ]
        ),
        "chunks_marked_processed": (
            marked_count
        ),
    }