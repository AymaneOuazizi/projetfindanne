from src.generation.service import generate_answer
from src.retrieval.hybrid import search_hybrid_chunks
from src.retrieval.schemas import HybridRetrievedChunk


def answer_question_hybrid(
    question: str,
    top_k: int = 5,
    candidate_limit: int = 10,
    rrf_k: int = 60,
) -> tuple[str, list[HybridRetrievedChunk]]:
    chunks = search_hybrid_chunks(
        query=question,
        limit=top_k,
        candidate_limit=candidate_limit,
        rrf_k=rrf_k,
    )

    answer = generate_answer(
        question=question,
        chunks=chunks,
    )

    return answer, chunks