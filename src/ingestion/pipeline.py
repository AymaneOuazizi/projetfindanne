from pathlib import Path

from src.database import SessionLocal
from src.ingestion.loaders import load_text_file
from src.ingestion.service import ingest_document


def ingest_directory(
    directory: str,
) -> int:
    directory_path = Path(directory)

    files = list(directory_path.glob("*.txt"))

    db = SessionLocal()
    ingested_count = 0

    try:
        for file_path in files:
            content = load_text_file(file_path)

            document = ingest_document(
                db=db,
                title=file_path.stem,
                source=str(file_path),
                content=content,
                language="en",
            )

            print(
                f"Ingested: {document.title} "
                f"(id={document.id})"
            )

            ingested_count += 1

        return ingested_count

    finally:
        db.close()