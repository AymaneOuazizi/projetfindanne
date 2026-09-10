from groq import Groq

from src.config import settings
from src.generation.graph_prompts import (
    build_graph_context,
)
from src.graph.search import (
    GraphSearchResult,
)


def generate_graph_answer(
    question: str,
    graph_result: GraphSearchResult,
) -> str:
    if not settings.groq_api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not configured."
        )

    if (
        not graph_result.relationships
        and not graph_result.evidence_chunks
    ):
        return (
            "The provided sources are "
            "insufficient to answer "
            "the question."
        )

    client = Groq(
        api_key=settings.groq_api_key
    )

    context = build_graph_context(
        graph_result
    )

    completion = (
        client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an assistant "
                        "specialized in SAP "
                        "knowledge. "
                        "Answer only using the "
                        "provided graph facts "
                        "and source evidence. "
                        "Do not use outside "
                        "knowledge. "
                        "Do not invent missing "
                        "relationships. "
                        "If the provided context "
                        "is insufficient, say "
                        "that the provided "
                        "sources are insufficient. "
                        "Cite textual evidence "
                        "using [SOURCE 1], "
                        "[SOURCE 2], etc. "
                        "Graph facts may help "
                        "you reason, but factual "
                        "claims must be supported "
                        "by the source evidence. "
                        "Be concise and factual."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"CONTEXT:\n\n"
                        f"{context}\n\n"
                        f"QUESTION:\n"
                        f"{question}"
                    ),
                },
            ],
            temperature=0.1,
            max_completion_tokens=2048,
            top_p=1,
            reasoning_effort="medium",
            stream=False,
        )
    )

    return (
        completion
        .choices[0]
        .message.content
        or ""
    )