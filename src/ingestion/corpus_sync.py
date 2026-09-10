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

SUPPORTED_EXTENSIONS = {
    ".txt",
    ".md",
    ".markdown",
}


def read_text_file(
    file_path: Path,
) -> str:
    return file_path.read_text(
        encoding="utf-8",
        errors="ignore",
    )


def sync_sap_corpus(
    corpus_dir: str = "data/raw/sap",
    sync_graph: bool = True,
) -> dict:
    corpus_path = Path(
        corpus_dir
    )

    if not corpus_path.exists():
        raise FileNotFoundError(
            "SAP corpus directory not found: "
            f"{corpus_path}"
        )

    files = [
        path
        for path in corpus_path.rglob("*")
        if (
            path.is_file()
            and path.suffix.lower()
            in SUPPORTED_EXTENSIONS
        )
    ]

    if not files:
        return {
            "files_found": 0,
            "documents_processed": 0,
            "embeddings_generated": 0,
            "graph_sync": None,
        }

    db = SessionLocal()

    documents_processed = 0

    try:
        for file_path in files:
            content = read_text_file(
                file_path
            )

            if not content.strip():
                print(
                    "Skipping empty file: "
                    f"{file_path}"
                )
                continue

            ingest_document(
                db=db,
                title=file_path.stem,
                source=str(file_path),
                content=content,
                language="en",
            )

            documents_processed += 1

    finally:
        db.close()

    embeddings_generated = (
        generate_missing_embeddings()
    )

    graph_sync = None

    if sync_graph:
        graph_sync = (
            sync_knowledge_graph_incrementally()
        )

    return {
        "files_found": len(
            files
        ),
        "documents_processed": (
            documents_processed
        ),
        "embeddings_generated": (
            embeddings_generated
        ),
        "graph_sync": graph_sync,
    }