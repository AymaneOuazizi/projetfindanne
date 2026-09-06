from dataclasses import dataclass


@dataclass
class RetrievedChunk:
    chunk_id: int
    document_id: int
    chunk_index: int
    content: str
    source: str
    title: str
    distance: float