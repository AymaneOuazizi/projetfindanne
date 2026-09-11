from dataclasses import dataclass

from src.graph.entity_search import (
    find_entities_in_question,
)
from src.graph.evidence import (
    get_graph_evidence,
)
from src.graph.retrieval_schemas import (
    GraphEntityMatch,
    GraphEvidenceChunk,
    GraphRelationResult,
)
from src.graph.retriever import (
    search_graph,
)


@dataclass
class GraphSearchResult:
    matched_entities: list[
        GraphEntityMatch
    ]

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
    matched_entities = (
        find_entities_in_question(
            question
        )
    )

    relationships = search_graph(
        question=question,
        max_hops=max_hops,
    )

    evidence_chunks = (
        get_graph_evidence(
            relationships=relationships,
            entities=matched_entities,
        )
    )

    return GraphSearchResult(
        matched_entities=matched_entities,
        relationships=relationships,
        evidence_chunks=evidence_chunks,
    )