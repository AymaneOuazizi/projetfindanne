from pathlib import Path

from src.database import SessionLocal
from src.embeddings.pipeline import (
    generate_missing_embeddings,
)
from src.graph.incremental import (
    sync_knowledge_graph_incrementally,
)
from src.ingestion.service import (
    ingest_document,
)
from src.ingestion.upload import (
    extract_uploaded_text,
)


def ingest_uploaded_files(
    file_paths: list[Path],
) -> list[dict]:
    ingested_documents = []

    db = SessionLocal()

    try:
        for file_path in file_paths:
            text = extract_uploaded_text(
                file_path
            )

            if not text.strip():
                raise ValueError(
                    "No readable text was extracted "
                    f"from {file_path.name}."
                )

            document = ingest_document(
                db=db,
                title=file_path.stem,
                source=str(file_path),
                content=text,
                language="en",
            )

            ingested_documents.append(
                {
                    "document_id": (
                        document.id
                    ),
                    "title": (
                        document.title
                    ),
                    "source": (
                        document.source
                    ),
                }
            )

        if ingested_documents:
            generate_missing_embeddings()

            sync_knowledge_graph_incrementally()

        return ingested_documents

    finally:
        db.close()