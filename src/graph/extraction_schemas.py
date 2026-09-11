from typing import Literal

from pydantic import BaseModel, Field

EntityType = Literal[
    # SAP/domain entities
    "Module",
    "Process",
    "BusinessObject",
    "Concept",

    # Generic entities for uploaded documents
    "Person",
    "Organization",
    "Location",
    "Product",
    "System",
]


RelationshipType = Literal[
    # SAP/domain relationships
    "CONTAINS_PROCESS",
    "USES_OBJECT",
    "PRECEDES",

    # Generic relationships
    "WORKS_AT",
    "STUDIES_AT",
    "MEMBER_OF",
    "PART_OF",
    "LOCATED_IN",
    "USES",
    "RELATED_TO",
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