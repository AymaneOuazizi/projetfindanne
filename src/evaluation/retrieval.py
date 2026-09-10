import json
import time
from pathlib import Path

from src.retrieval.vector import search_similar_chunks


def load_evaluation_dataset(
    file_path: str,
) -> list[dict]:
    path = Path(file_path)

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def evaluate_retrieval(
    dataset_path: str,
    top_k: int = 3,
) -> dict:
    dataset = load_evaluation_dataset(
        dataset_path
    )

    evaluated_questions = 0
    recall_hits = 0
    reciprocal_rank_sum = 0.0
    total_latency_ms = 0.0

    results = []

    for item in dataset:
        question = item["question"]
        expected_document = item[
            "expected_document"
        ]

        if expected_document is None:
            continue

        start_time = time.perf_counter()

        retrieved_chunks = search_similar_chunks(
            query=question,
            limit=top_k,
        )

        end_time = time.perf_counter()

        latency_ms = (
            end_time - start_time
        ) * 1000

        total_latency_ms += latency_ms

        retrieved_documents = [
            chunk.title
            for chunk in retrieved_chunks
        ]

        evaluated_questions += 1

        hit = (
            expected_document
            in retrieved_documents
        )

        if hit:
            recall_hits += 1

            rank = (
                retrieved_documents.index(
                    expected_document
                )
                + 1
            )

            reciprocal_rank_sum += 1 / rank
        else:
            rank = None

        results.append(
            {
                "id": item["id"],
                "question": question,
                "expected_document": expected_document,
                "retrieved_documents": retrieved_documents,
                "hit": hit,
                "rank": rank,
                "latency_ms": latency_ms,
            }
        )

    if evaluated_questions == 0:
        recall_at_k = 0.0
        mrr = 0.0
        average_latency_ms = 0.0
    else:
        recall_at_k = (
            recall_hits
            / evaluated_questions
        )

        mrr = (
            reciprocal_rank_sum
            / evaluated_questions
        )

        average_latency_ms = (
            total_latency_ms
            / evaluated_questions
        )

    return {
        "top_k": top_k,
        "questions_evaluated": evaluated_questions,
        "recall_at_k": recall_at_k,
        "mrr": mrr,
        "average_latency_ms": average_latency_ms,
        "results": results,
    }