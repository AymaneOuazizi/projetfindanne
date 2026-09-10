from src.config import settings
from src.graph.database import driver
from src.graph.normalization import (
    normalize_entity_id,
)
from src.graph.retrieval_schemas import (
    GraphEntityMatch,
)


SEARCHABLE_LABELS = {
    "Module",
    "Process",
    "BusinessObject",
    "Concept",
}


def find_entities_in_question(
    question: str,
) -> list[GraphEntityMatch]:
    normalized_question = (
        normalize_entity_id(
            question
        )
    )

    matches = []

    with driver.session(
        database=settings.neo4j_database
    ) as session:

        records = session.run(
            """
            MATCH (entity)

            WHERE entity.entity_id IS NOT NULL

            RETURN
                entity.entity_id
                    AS entity_id,
                entity.name
                    AS name,
                labels(entity)[0]
                    AS label
            """
        )

        for record in records:
            label = record["label"]

            if (
                label
                not in SEARCHABLE_LABELS
            ):
                continue

            entity_id = (
                record["entity_id"]
            )

            if not entity_id:
                continue

            if (
                entity_id
                in normalized_question
            ):
                matches.append(
                    GraphEntityMatch(
                        entity_id=(
                            entity_id
                        ),
                        name=record[
                            "name"
                        ],
                        label=label,
                    )
                )

    matches.sort(
        key=lambda match: len(
            match.entity_id
        ),
        reverse=True,
    )

    return matches