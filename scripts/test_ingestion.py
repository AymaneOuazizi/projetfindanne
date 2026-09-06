from src.database import SessionLocal
from src.ingestion.service import ingest_document


def main():
    sample_text = """
    SAP Materials Management is a module used for procurement,
    inventory management, material planning, and vendor management.

    It helps organizations manage materials and purchasing processes.
    """

    db = SessionLocal()

    try:
        document = ingest_document(
            db=db,
            title="SAP MM Test Document",
            source="manual-test",
            content=sample_text,
            language="en",
        )

        print(f"Document ID: {document.id}")
        print(f"Title: {document.title}")
        print(f"Hash: {document.content_hash}")

    finally:
        db.close()


if __name__ == "__main__":
    main()