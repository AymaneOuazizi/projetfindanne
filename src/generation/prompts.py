from src.retrieval.schemas import RetrievedChunk


def build_context(
    chunks: list[RetrievedChunk],
) -> str:
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