from src.retrieval.bm25 import (
    search_bm25_chunks,
)
from src.retrieval.fusion import (
    reciprocal_rank_fusion,
)
from src.retrieval.schemas import (
    HybridRetrievedChunk,
)
from src.retrieval.vector import (
    search_similar_chunks,
)


def search_hybrid_chunks(
    query: str,
    limit: int = 5,
    candidate_limit: int = 10,
    rrf_k: int = 60,
) -> list[HybridRetrievedChunk]:
    vector_results = search_similar_chunks(
        query=query,
        limit=candidate_limit,
    )

    bm25_results = search_bm25_chunks(
        query=query,
        limit=candidate_limit,
    )

    hybrid_results = reciprocal_rank_fusion(
        vector_results=vector_results,
        bm25_results=bm25_results,
        limit=limit,
        rrf_k=rrf_k,
    )

    return hybrid_results