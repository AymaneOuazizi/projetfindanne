from groq import Groq

from src.config import settings
from src.generation.prompts import build_context
from src.retrieval.schemas import RetrievedChunk


def generate_answer(
    question: str,
    chunks: list[RetrievedChunk],
) -> str:
    if not settings.groq_api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not configured."
        )

    client = Groq(
        api_key=settings.groq_api_key,
    )

    context = build_context(chunks)

    completion = client.chat.completions.create(
        model=settings.llm_model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an assistant specialized in SAP knowledge. "
                    "Answer the user's question only using the provided "
                    "context. Do not invent information. "
                    "If the answer is not supported by the context, "
                    "say that the provided sources are insufficient. "
                    "Cite sources using [SOURCE 1], [SOURCE 2], etc. "
                    "Be concise and factual."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"CONTEXT:\n\n{context}\n\n"
                    f"QUESTION:\n{question}"
                ),
            },
        ],
        temperature=0.1,
        max_completion_tokens=2048,
        top_p=1,
        reasoning_effort="medium",
        stream=False,
    )

    return completion.choices[0].message.content or ""