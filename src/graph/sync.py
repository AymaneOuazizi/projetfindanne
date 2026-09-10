from src.config import settings
from src.database import SessionLocal
from src.graph.database import driver
from src.models.chunk import Chunk
from src.models.document import Document


def fetch_postgres_documents(
    document_ids: list[int] | None = None,
) -> list[dict]:
    with SessionLocal() as session:
        query = session.query(Document)

        if document_ids is not None:
            if not document_ids:
                return []

            query = query.filter(
                Document.id.in_(document_ids)
            )

        documents = (
            query
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


def fetch_postgres_chunks(
    chunk_ids: list[int] | None = None,
) -> list[dict]:
    with SessionLocal() as session:
        query = (
            session.query(
                Chunk,
                Document,
            )
            .join(
                Document,
                Chunk.document_id
                == Document.id,
            )
        )

        if chunk_ids is not None:
            if not chunk_ids:
                return []

            query = query.filter(
                Chunk.id.in_(chunk_ids)
            )

        chunks = (
            query
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


def sync_postgres_to_neo4j(
    document_ids: list[int] | None = None,
    chunk_ids: list[int] | None = None,
) -> dict:
    documents = fetch_postgres_documents(
        document_ids=document_ids
    )

    chunks = fetch_postgres_chunks(
        chunk_ids=chunk_ids
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