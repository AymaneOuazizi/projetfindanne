import re
import time
import unicodedata

from src.evaluation.retrieval import load_evaluation_dataset
from src.generation.rag import answer_question


def normalize_text(text: str) -> str:
    return unicodedata.normalize(
        "NFKC",
        text,
    ).lower()


def has_source_citation(answer: str) -> bool:
    normalized_answer = normalize_text(answer)

    patterns = [
        r"\[\s*source\s*\d+\s*\]",
        r"【\s*source\s*\d+\s*】",
    ]

    return any(
        re.search(pattern, normalized_answer)
        for pattern in patterns
    )


def is_refusal(answer: str) -> bool:
    normalized_answer = normalize_text(answer)

    refusal_phrases = [
        "provided sources are insufficient",
        "sources are insufficient",
        "not enough information",
        "cannot answer",
        "can't answer",
        "cannot be derived",
        "not supported by the context",
        "not supported by the provided context",
        "do not contain information",
        "does not contain information",
        "do not include",
        "does not include",
        "context is insufficient",
    ]

    return any(
        phrase in normalized_answer
        for phrase in refusal_phrases
    )


def evaluate_generation(
    dataset_path: str,
    top_k: int = 3,
) -> dict:
    dataset = load_evaluation_dataset(
        dataset_path
    )

    total_questions = 0

    answerable_questions = 0
    citation_hits = 0

    unanswerable_questions = 0
    refusal_hits = 0

    total_latency_ms = 0.0

    results = []

    for item in dataset:
        question = item["question"]
        expected_document = item[
            "expected_document"
        ]

        # Start measuring full RAG latency
        start_time = time.perf_counter()

        answer, chunks = answer_question(
            question=question,
            top_k=top_k,
        )

        # Stop measuring latency
        end_time = time.perf_counter()

        latency_ms = (
            end_time - start_time
        ) * 1000

        total_latency_ms += latency_ms

        total_questions += 1

        citation = has_source_citation(
            answer
        )

        refusal = is_refusal(
            answer
        )

        if expected_document is not None:
            answerable_questions += 1

            if citation:
                citation_hits += 1

            correct_refusal_behavior = (
                not refusal
            )

        else:
            unanswerable_questions += 1

            if refusal:
                refusal_hits += 1

            correct_refusal_behavior = (
                refusal
            )

        results.append(
            {
                "id": item["id"],
                "question": question,
                "expected_document": (
                    expected_document
                ),
                "answer": answer,
                "has_citation": citation,
                "is_refusal": refusal,
                "correct_refusal_behavior": (
                    correct_refusal_behavior
                ),
                "latency_ms": latency_ms,
                "retrieved_sources": [
                    chunk.title
                    for chunk in chunks
                ],
            }
        )

    citation_rate = (
        citation_hits
        / answerable_questions
        if answerable_questions
        else 0.0
    )

    refusal_accuracy = (
        refusal_hits
        / unanswerable_questions
        if unanswerable_questions
        else 0.0
    )

    average_latency_ms = (
        total_latency_ms
        / total_questions
        if total_questions
        else 0.0
    )

    return {
        "questions_evaluated": (
            total_questions
        ),
        "answerable_questions": (
            answerable_questions
        ),
        "unanswerable_questions": (
            unanswerable_questions
        ),
        "citation_rate": citation_rate,
        "refusal_accuracy": (
            refusal_accuracy
        ),
        "average_latency_ms": (
            average_latency_ms
        ),
        "results": results,
    }