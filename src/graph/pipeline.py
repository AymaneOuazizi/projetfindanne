from src.database import SessionLocal
from src.graph.extraction import (
    extract_graph_from_text,
)
from src.graph.writer import (
    write_extraction_to_graph,
)
from src.models.chunk import Chunk
from src.models.document import Document


def load_chunks_for_extraction() -> list[dict]:
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
            .order_by(
                Document.id,
                Chunk.chunk_index,
            )
            .all()
        )

        return [
            {
                "chunk_id": chunk.id,
                "chunk_index": (
                    chunk.chunk_index
                ),
                "content": chunk.content,
                "document_id": (
                    document.id
                ),
                "document_title": (
                    document.title
                ),
            }
            for chunk, document in rows
        ]


def process_chunk(
    chunk: dict,
) -> dict:
    extraction = extract_graph_from_text(
        chunk["content"]
    )

    write_result = (
        write_extraction_to_graph(
            extraction=extraction,
            source_chunk_id=(
                chunk["chunk_id"]
            ),
        )
    )

    return {
        "chunk_id": chunk["chunk_id"],
        "chunk_index": (
            chunk["chunk_index"]
        ),
        "document_id": (
            chunk["document_id"]
        ),
        "document_title": (
            chunk["document_title"]
        ),
        "entities_extracted": len(
            extraction.entities
        ),
        "relationships_extracted": len(
            extraction.relationships
        ),
        "entities_written": (
            write_result[
                "entities_written"
            ]
        ),
        "relationships_written": (
            write_result[
                "relationships_written"
            ]
        ),
    }


def run_graph_extraction_pipeline() -> dict:
    chunks = load_chunks_for_extraction()

    processed = 0
    failed = 0

    total_entities = 0
    total_relationships = 0

    results = []

    for chunk in chunks:
        try:
            result = process_chunk(
                chunk
            )

            processed += 1

            total_entities += (
                result[
                    "entities_extracted"
                ]
            )

            total_relationships += (
                result[
                    "relationships_extracted"
                ]
            )

            results.append(
                {
                    **result,
                    "status": "success",
                    "error": None,
                }
            )

        except Exception as error:
            failed += 1

            results.append(
                {
                    "chunk_id": (
                        chunk["chunk_id"]
                    ),
                    "chunk_index": (
                        chunk[
                            "chunk_index"
                        ]
                    ),
                    "document_id": (
                        chunk["document_id"]
                    ),
                    "document_title": (
                        chunk[
                            "document_title"
                        ]
                    ),
                    "status": "failed",
                    "error": str(error),
                }
            )

    return {
        "chunks_total": len(chunks),
        "chunks_processed": processed,
        "chunks_failed": failed,
        "entities_extracted": (
            total_entities
        ),
        "relationships_extracted": (
            total_relationships
        ),
        "results": results,
    }