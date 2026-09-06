from src.generation.service import generate_answer
from src.retrieval.schemas import RetrievedChunk
from src.retrieval.vector import search_similar_chunks


def answer_question(
    question: str,
    top_k: int = 5,
) -> tuple[str, list[RetrievedChunk]]:
    chunks = search_similar_chunks(
        query=question,
        limit=top_k,
    )

    answer = generate_answer(
        question=question,
        chunks=chunks,
    )

    return answer, chunks