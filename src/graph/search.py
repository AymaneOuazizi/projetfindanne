from dataclasses import dataclass

from src.graph.evidence import (
    get_graph_evidence,
)
from src.graph.retrieval_schemas import (
    GraphEvidenceChunk,
    GraphRelationResult,
)
from src.graph.retriever import (
    search_graph,
)


@dataclass
class GraphSearchResult:
    relationships: list[
        GraphRelationResult
    ]

    evidence_chunks: list[
        GraphEvidenceChunk
    ]


def search_graph_with_evidence(
    question: str,
    max_hops: int = 2,
) -> GraphSearchResult:
    relationships = search_graph(
        question=question,
        max_hops=max_hops,
    )

    evidence_chunks = (
        get_graph_evidence(
            relationships
        )
    )

    return GraphSearchResult(
        relationships=relationships,
        evidence_chunks=evidence_chunks,
    )