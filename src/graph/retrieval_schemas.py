from dataclasses import dataclass


@dataclass
class GraphEntityMatch:
    entity_id: str
    name: str
    label: str


@dataclass
class GraphRelationResult:
    source_id: str
    source_name: str
    source_type: str

    relationship: str

    target_id: str
    target_name: str
    target_type: str

    direction: str

    source_chunk_ids: list[int]


@dataclass
class GraphEvidenceChunk:
    chunk_id: int
    document_id: int
    chunk_index: int
    content: str
    source: str
    title: str