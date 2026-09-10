from typing import Literal

from pydantic import BaseModel, Field


EntityType = Literal[
    "Module",
    "Process",
    "BusinessObject",
    "Concept",
]


RelationshipType = Literal[
    "CONTAINS_PROCESS",
    "USES_OBJECT",
    "PRECEDES",
]


class ExtractedEntity(BaseModel):
    name: str = Field(
        min_length=1,
        description=(
            "Canonical human-readable "
            "name of the entity."
        ),
    )

    type: EntityType


class ExtractedRelationship(BaseModel):
    source: str = Field(
        min_length=1,
    )

    target: str = Field(
        min_length=1,
    )

    type: RelationshipType


class GraphExtraction(BaseModel):
    entities: list[ExtractedEntity] = (
        Field(default_factory=list)
    )

    relationships: list[
        ExtractedRelationship
    ] = Field(default_factory=list)