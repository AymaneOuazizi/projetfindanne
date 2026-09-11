from src.config import settings
from src.database import SessionLocal
from src.graph.database import driver
from src.graph.retrieval_schemas import (
    GraphEntityMatch,
    GraphEvidenceChunk,
    GraphRelationResult,
)
from src.models.chunk import Chunk
from src.models.document import Document


def collect_relationship_source_chunk_ids(
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
                int(chunk_id)
            )

    return sorted(chunk_ids)


def collect_entity_source_chunk_ids(
    entities: list[
        GraphEntityMatch
    ],
) -> list[int]:
    if not entities:
        return []

    entity_ids = [
        entity.entity_id
        for entity in entities
    ]

    chunk_ids = set()

    with driver.session(
        database=settings.neo4j_database
    ) as session:

        records = session.run(
            """
            MATCH (entity)-[:SUPPORTED_BY]->
                  (chunk:Chunk)

            WHERE entity.entity_id IN $entity_ids

            RETURN DISTINCT
                chunk.postgres_id
                    AS chunk_id
            """,
            entity_ids=entity_ids,
        )

        for record in records:
            chunk_id = record[
                "chunk_id"
            ]

            if chunk_id is None:
                continue

            chunk_ids.add(
                int(chunk_id)
            )

    return sorted(chunk_ids)


def collect_source_chunk_ids(
    relationships: list[
        GraphRelationResult
    ],
    entities: list[
        GraphEntityMatch
    ] | None = None,
) -> list[int]:
    relationship_chunk_ids = (
        collect_relationship_source_chunk_ids(
            relationships
        )
    )

    entity_chunk_ids = (
        collect_entity_source_chunk_ids(
            entities or []
        )
    )

    return sorted(
        set(
            relationship_chunk_ids
        )
        | set(
            entity_chunk_ids
        )
    )


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
    entities: list[
        GraphEntityMatch
    ] | None = None,
) -> list[GraphEvidenceChunk]:
    chunk_ids = (
        collect_source_chunk_ids(
            relationships=relationships,
            entities=entities,
        )
    )

    return load_evidence_chunks(
        chunk_ids
    )