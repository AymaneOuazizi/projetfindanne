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

@dataclass
class BM25RetrievedChunk:
    chunk_id: int
    document_id: int
    chunk_index: int
    content: str
    source: str
    title: str
    score: float

@dataclass
class HybridRetrievedChunk:
    chunk_id: int
    document_id: int
    chunk_index: int
    content: str
    source: str
    title: str
    rrf_score: float