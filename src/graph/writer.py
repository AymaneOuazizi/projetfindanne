from src.config import settings
from src.graph.database import driver
from src.graph.extraction_schemas import (
    GraphExtraction,
)
from src.graph.normalization import (
    normalize_entity_id,
)

ALLOWED_LABELS = {
    "Module",
    "Process",
    "BusinessObject",
    "Concept",
}


ALLOWED_RELATIONSHIPS = {
    "CONTAINS_PROCESS",
    "USES_OBJECT",
    "PRECEDES",
}


def merge_entity(
    session,
    entity_name: str,
    entity_type: str,
    source_chunk_id: int,
) -> None:
    if entity_type not in ALLOWED_LABELS:
        raise ValueError(
            f"Unsupported entity type: "
            f"{entity_type}"
        )

    entity_id = normalize_entity_id(
        entity_name
    )

    if not entity_id:
        return

    query = f"""
    MERGE (
        entity:{entity_type} {{
            entity_id: $entity_id
        }}
    )

    SET
        entity.name = $entity_name

    WITH entity

    MATCH (
        chunk:Chunk {{
            postgres_id: $source_chunk_id
        }}
    )

    MERGE (
        entity
    )-[:SUPPORTED_BY]->(
        chunk
    )
    """

    session.run(
        query,
        entity_id=entity_id,
        entity_name=entity_name,
        source_chunk_id=source_chunk_id,
    ).consume()


def merge_relationship(
    session,
    source_name: str,
    target_name: str,
    relationship_type: str,
    source_chunk_id: int,
) -> None:
    if (
        relationship_type
        not in ALLOWED_RELATIONSHIPS
    ):
        raise ValueError(
            "Unsupported relationship type: "
            f"{relationship_type}"
        )

    source_id = normalize_entity_id(
        source_name
    )

    target_id = normalize_entity_id(
        target_name
    )

    if not source_id or not target_id:
        return

    query = f"""
    MATCH (
        source {{
            entity_id: $source_id
        }}
    )

    MATCH (
        target {{
            entity_id: $target_id
        }}
    )

    MERGE (
        source
    )-[relationship:{relationship_type}]->(
        target
    )

    SET
        relationship.source_chunk_id =
            $source_chunk_id
    """

    session.run(
        query,
        source_id=source_id,
        target_id=target_id,
        source_chunk_id=source_chunk_id,
    ).consume()


def write_extraction_to_graph(
    extraction: GraphExtraction,
    source_chunk_id: int,
) -> dict:
    entities_written = 0
    relationships_written = 0

    with driver.session(
        database=settings.neo4j_database
    ) as session:

        for entity in extraction.entities:
            merge_entity(
                session=session,
                entity_name=entity.name,
                entity_type=entity.type,
                source_chunk_id=(
                    source_chunk_id
                ),
            )

            entities_written += 1

        for relationship in (
            extraction.relationships
        ):
            merge_relationship(
                session=session,
                source_name=(
                    relationship.source
                ),
                target_name=(
                    relationship.target
                ),
                relationship_type=(
                    relationship.type
                ),
                source_chunk_id=(
                    source_chunk_id
                ),
            )

            relationships_written += 1

    return {
        "entities_written": (
            entities_written
        ),
        "relationships_written": (
            relationships_written
        ),
    }