from dataclasses import dataclass

from src.generation.graph_rag import (
    answer_question_graph,
)
from src.generation.hybrid_rag import (
    answer_question_hybrid,
)
from src.generation.rag import (
    answer_question,
)


@dataclass
class UnifiedRAGResult:
    architecture: str
    answer: str
    sources: list[dict]


def ask_rag(
    question: str,
    architecture: str,
) -> UnifiedRAGResult:
    architecture = (
        architecture
        .strip()
        .lower()
    )

    if architecture == "vector":
        answer, chunks = (
            answer_question(
                question
            )
        )

        sources = [
            {
                "chunk_id": (
                    chunk.chunk_id
                ),
                "title": (
                    chunk.title
                ),
                "source": (
                    chunk.source
                ),
                "content": (
                    chunk.content
                ),
            }
            for chunk in chunks
        ]

    elif architecture == "hybrid":
        answer, chunks = (
            answer_question_hybrid(
                question
            )
        )

        sources = [
            {
                "chunk_id": (
                    chunk.chunk_id
                ),
                "title": (
                    chunk.title
                ),
                "source": (
                    chunk.source
                ),
                "content": (
                    chunk.content
                ),
            }
            for chunk in chunks
        ]

    elif architecture == "graph":
        answer, graph_result = (
            answer_question_graph(
                question=question,
                max_hops=2,
            )
        )

        sources = [
            {
                "chunk_id": (
                    chunk.chunk_id
                ),
                "title": (
                    chunk.title
                ),
                "source": (
                    chunk.source
                ),
                "content": (
                    chunk.content
                ),
            }
            for chunk
            in graph_result.evidence_chunks
        ]

    else:
        raise ValueError(
            "Unsupported RAG architecture: "
            f"{architecture}"
        )

    return UnifiedRAGResult(
        architecture=architecture,
        answer=answer,
        sources=sources,
    )