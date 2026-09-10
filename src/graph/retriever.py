from src.config import settings
from src.graph.database import driver
from src.graph.entity_search import (
    find_entities_in_question,
)
from src.graph.retrieval_schemas import (
    GraphRelationResult,
)

ALLOWED_GRAPH_RELATIONSHIPS = {
    "CONTAINS_PROCESS",
    "USES_OBJECT",
    "PRECEDES",
}


def _extract_chunk_ids(
    record,
) -> list[int]:
    plural_ids = record.get(
        "source_chunk_ids"
    )

    singular_id = record.get(
        "source_chunk_id"
    )

    if plural_ids:
        return list(plural_ids)

    if singular_id is not None:
        return [singular_id]

    return []


def retrieve_outgoing_relationships(
    entity_id: str,
) -> list[GraphRelationResult]:
    with driver.session(
        database=settings.neo4j_database
    ) as session:

        records = session.run(
            """
            MATCH (
                source {
                    entity_id: $entity_id
                }
            )-[relationship]->(
                target
            )

            WHERE
                target.entity_id IS NOT NULL
                AND type(relationship)
                    IN $allowed_relationships

            RETURN
                source.entity_id
                    AS source_id,

                source.name
                    AS source_name,

                labels(source)[0]
                    AS source_type,

                type(relationship)
                    AS relationship,

                target.entity_id
                    AS target_id,

                target.name
                    AS target_name,

                labels(target)[0]
                    AS target_type,

                relationship[
                    $plural_property
                ]
                    AS source_chunk_ids,

                relationship[
                    $singular_property
                ]
                    AS source_chunk_id
            """,
            entity_id=entity_id,
            allowed_relationships=list(
                ALLOWED_GRAPH_RELATIONSHIPS
            ),
            plural_property=(
                "source_chunk_ids"
            ),
            singular_property=(
                "source_chunk_id"
            ),
        )

        results = []

        for record in records:
            results.append(
                GraphRelationResult(
                    source_id=record[
                        "source_id"
                    ],
                    source_name=record[
                        "source_name"
                    ],
                    source_type=record[
                        "source_type"
                    ],
                    relationship=record[
                        "relationship"
                    ],
                    target_id=record[
                        "target_id"
                    ],
                    target_name=record[
                        "target_name"
                    ],
                    target_type=record[
                        "target_type"
                    ],
                    direction="outgoing",
                    source_chunk_ids=(
                        _extract_chunk_ids(
                            record
                        )
                    ),
                )
            )

        return results


def retrieve_incoming_relationships(
    entity_id: str,
) -> list[GraphRelationResult]:
    with driver.session(
        database=settings.neo4j_database
    ) as session:

        records = session.run(
            """
            MATCH (
                source
            )-[relationship]->(
                target {
                    entity_id: $entity_id
                }
            )

            WHERE
                source.entity_id IS NOT NULL
                AND type(relationship)
                    IN $allowed_relationships

            RETURN
                source.entity_id
                    AS source_id,

                source.name
                    AS source_name,

                labels(source)[0]
                    AS source_type,

                type(relationship)
                    AS relationship,

                target.entity_id
                    AS target_id,

                target.name
                    AS target_name,

                labels(target)[0]
                    AS target_type,

                relationship[
                    $plural_property
                ]
                    AS source_chunk_ids,

                relationship[
                    $singular_property
                ]
                    AS source_chunk_id
            """,
            entity_id=entity_id,
            allowed_relationships=list(
                ALLOWED_GRAPH_RELATIONSHIPS
            ),
            plural_property=(
                "source_chunk_ids"
            ),
            singular_property=(
                "source_chunk_id"
            ),
        )

        results = []

        for record in records:
            results.append(
                GraphRelationResult(
                    source_id=record[
                        "source_id"
                    ],
                    source_name=record[
                        "source_name"
                    ],
                    source_type=record[
                        "source_type"
                    ],
                    relationship=record[
                        "relationship"
                    ],
                    target_id=record[
                        "target_id"
                    ],
                    target_name=record[
                        "target_name"
                    ],
                    target_type=record[
                        "target_type"
                    ],
                    direction="incoming",
                    source_chunk_ids=(
                        _extract_chunk_ids(
                            record
                        )
                    ),
                )
            )

        return results


def retrieve_entity_neighborhood(
    entity_id: str,
) -> list[GraphRelationResult]:
    results = []

    results.extend(
        retrieve_outgoing_relationships(
            entity_id
        )
    )

    results.extend(
        retrieve_incoming_relationships(
            entity_id
        )
    )

    unique_results = []
    seen = set()

    for result in results:
        key = (
            result.source_id,
            result.relationship,
            result.target_id,
        )

        if key in seen:
            continue

        seen.add(key)

        unique_results.append(
            result
        )

    return unique_results


def search_graph(
    question: str,
    max_hops: int = 2,
) -> list[GraphRelationResult]:
    matched_entities = (
        find_entities_in_question(
            question
        )
    )

    if not matched_entities:
        return []

    all_results = []
    seen_relationships = set()

    visited_entities = set()

    frontier = {
        entity.entity_id
        for entity in matched_entities
    }

    for _ in range(max_hops):
        if not frontier:
            break

        next_frontier = set()

        for entity_id in frontier:
            if entity_id in visited_entities:
                continue

            visited_entities.add(
                entity_id
            )

            relationships = (
                retrieve_entity_neighborhood(
                    entity_id
                )
            )

            for relationship in relationships:
                key = (
                    relationship.source_id,
                    relationship.relationship,
                    relationship.target_id,
                )

                if key not in seen_relationships:
                    seen_relationships.add(
                        key
                    )

                    all_results.append(
                        relationship
                    )

                if (
                    relationship.source_id
                    not in visited_entities
                ):
                    next_frontier.add(
                        relationship.source_id
                    )

                if (
                    relationship.target_id
                    not in visited_entities
                ):
                    next_frontier.add(
                        relationship.target_id
                    )

        frontier = next_frontier

    return all_results