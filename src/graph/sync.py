from src.config import settings
from src.database import SessionLocal
from src.graph.database import driver
from src.models.chunk import Chunk
from src.models.document import Document


def fetch_postgres_documents() -> list[dict]:
    with SessionLocal() as session:
        documents = (
            session.query(Document)
            .order_by(Document.id)
            .all()
        )

        return [
            {
                "postgres_id": document.id,
                "title": document.title,
                "source": document.source,
                "language": document.language,
                "content_hash": document.content_hash,
            }
            for document in documents
        ]


def fetch_postgres_chunks() -> list[dict]:
    with SessionLocal() as session:
        chunks = (
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
                "postgres_id": chunk.id,
                "document_postgres_id": (
                    document.id
                ),
                "chunk_index": (
                    chunk.chunk_index
                ),
                "content": chunk.content,
                "document_title": (
                    document.title
                ),
            }
            for chunk, document in chunks
        ]


def sync_documents_to_neo4j(
    documents: list[dict],
) -> int:
    if not documents:
        return 0

    with driver.session(
        database=settings.neo4j_database
    ) as session:
        session.run(
            """
            UNWIND $documents AS document

            MERGE (
                d:Document {
                    postgres_id:
                        document.postgres_id
                }
            )

            SET
                d.title =
                    document.title,
                d.source =
                    document.source,
                d.language =
                    document.language,
                d.content_hash =
                    document.content_hash
            """,
            documents=documents,
        ).consume()

    return len(documents)


def sync_chunks_to_neo4j(
    chunks: list[dict],
) -> int:
    if not chunks:
        return 0

    with driver.session(
        database=settings.neo4j_database
    ) as session:
        session.run(
            """
            UNWIND $chunks AS chunk

            MERGE (
                c:Chunk {
                    postgres_id:
                        chunk.postgres_id
                }
            )

            SET
                c.chunk_index =
                    chunk.chunk_index,
                c.content =
                    chunk.content

            WITH c, chunk

            MATCH (
                d:Document {
                    postgres_id:
                        chunk.document_postgres_id
                }
            )

            MERGE (
                d
            )-[:HAS_CHUNK]->(
                c
            )
            """,
            chunks=chunks,
        ).consume()

    return len(chunks)


def sync_postgres_to_neo4j() -> dict:
    documents = (
        fetch_postgres_documents()
    )

    chunks = (
        fetch_postgres_chunks()
    )

    synced_documents = (
        sync_documents_to_neo4j(
            documents
        )
    )

    synced_chunks = (
        sync_chunks_to_neo4j(
            chunks
        )
    )

    return {
        "documents": synced_documents,
        "chunks": synced_chunks,
    }