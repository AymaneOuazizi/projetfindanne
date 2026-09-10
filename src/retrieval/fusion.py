from collections import defaultdict

from src.retrieval.schemas import (
    BM25RetrievedChunk,
    HybridRetrievedChunk,
    RetrievedChunk,
)


def reciprocal_rank_fusion(
    vector_results: list[RetrievedChunk],
    bm25_results: list[BM25RetrievedChunk],
    limit: int = 5,
    rrf_k: int = 60,
) -> list[HybridRetrievedChunk]:
    scores = defaultdict(float)
    chunk_data = {}

    for rank, result in enumerate(
        vector_results,
        start=1,
    ):
        scores[result.chunk_id] += (
            1 / (rrf_k + rank)
        )

        chunk_data[result.chunk_id] = result

    for rank, result in enumerate(
        bm25_results,
        start=1,
    ):
        scores[result.chunk_id] += (
            1 / (rrf_k + rank)
        )

        chunk_data[result.chunk_id] = result

    ranked_chunk_ids = sorted(
        scores,
        key=scores.get,
        reverse=True,
    )

    fused_results = []

    for chunk_id in ranked_chunk_ids[:limit]:
        result = chunk_data[chunk_id]

        fused_results.append(
            HybridRetrievedChunk(
                chunk_id=result.chunk_id,
                document_id=result.document_id,
                chunk_index=result.chunk_index,
                content=result.content,
                source=result.source,
                title=result.title,
                rrf_score=scores[chunk_id],
            )
        )

    return fused_results