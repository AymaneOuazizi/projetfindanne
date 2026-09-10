import json
import re

from groq import Groq
from pydantic import ValidationError

from src.config import settings
from src.graph.extraction_prompts import (
    build_graph_extraction_prompt,
)
from src.graph.extraction_schemas import (
    ExtractedRelationship,
    GraphExtraction,
)
from src.graph.normalization import (
    normalize_entity_id,
)


def clean_json_response(
    response: str,
) -> str:
    response = response.strip()

    response = re.sub(
        r"^```json\s*",
        "",
        response,
        flags=re.IGNORECASE,
    )

    response = re.sub(
        r"^```\s*",
        "",
        response,
    )

    response = re.sub(
        r"\s*```$",
        "",
        response,
    )

    return response.strip()


def validate_relationship_endpoints(
    extraction: GraphExtraction,
) -> GraphExtraction:
    entity_names = {
        entity.name.strip().lower()
        for entity in extraction.entities
    }

    valid_relationships = []

    for relationship in (
        extraction.relationships
    ):
        source_exists = (
            relationship.source
            .strip()
            .lower()
            in entity_names
        )

        target_exists = (
            relationship.target
            .strip()
            .lower()
            in entity_names
        )

        if (
            source_exists
            and target_exists
        ):
            valid_relationships.append(
                relationship
            )

    extraction.relationships = (
        valid_relationships
    )

    return extraction


def deduplicate_extraction(
    extraction: GraphExtraction,
) -> GraphExtraction:
    unique_entities = {}

    for entity in extraction.entities:
        entity_id = normalize_entity_id(
            entity.name
        )

        if not entity_id:
            continue

        key = (
            entity.type,
            entity_id,
        )

        if key not in unique_entities:
            unique_entities[key] = entity

    extraction.entities = list(
        unique_entities.values()
    )

    unique_relationships = {}

    for relationship in (
        extraction.relationships
    ):
        key = (
            normalize_entity_id(
                relationship.source
            ),
            relationship.type,
            normalize_entity_id(
                relationship.target
            ),
        )

        if key not in unique_relationships:
            unique_relationships[key] = (
                relationship
            )

    extraction.relationships = list(
        unique_relationships.values()
    )

    return extraction


def extract_graph_from_text(
    text: str,
) -> GraphExtraction:
    if not settings.groq_api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not configured."
        )

    if not text.strip():
        return GraphExtraction()

    client = Groq(
        api_key=settings.groq_api_key
    )

    prompt = (
        build_graph_extraction_prompt(
            text
        )
    )

    completion = (
        client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a strict "
                        "information extraction "
                        "system. "
                        "Return valid JSON only."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0,
            max_completion_tokens=2048,
            top_p=1,
            stream=False,
        )
    )

    raw_response = (
        completion
        .choices[0]
        .message.content
        or ""
    )

    cleaned_response = (
        clean_json_response(
            raw_response
        )
    )

    try:
        parsed = json.loads(
            cleaned_response
        )

        extraction = (
            GraphExtraction.model_validate(
                parsed
            )
        )

    except (
        json.JSONDecodeError,
        ValidationError,
    ) as error:
        raise ValueError(
            "Invalid graph extraction "
            "returned by the LLM.\n\n"
            f"Raw response:\n"
            f"{raw_response}"
        ) from error

    extraction = (
        deduplicate_extraction(
            extraction
        )
    )

    extraction = (
        validate_relationship_endpoints(
            extraction
        )
    )

    return extraction