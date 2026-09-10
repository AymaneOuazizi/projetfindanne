from src.retrieval.schemas import (
    BM25RetrievedChunk,
    HybridRetrievedChunk,
    RetrievedChunk,
)

RAGChunk = (RetrievedChunk| BM25RetrievedChunk| HybridRetrievedChunk)

def build_context(chunks: list[RAGChunk],) -> str:
    context_parts = []

    for index, chunk in enumerate(chunks, start=1):
        context_parts.append(
            f"""
[SOURCE {index}]
Title: {chunk.title}
Source: {chunk.source}

{chunk.content}
""".strip()
        )

    return "\n\n".join(context_parts)