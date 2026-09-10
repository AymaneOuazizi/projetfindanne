import json
import time
from pathlib import Path

from src.graph.search import (
    search_graph_with_evidence,
)


def load_evaluation_questions(
    dataset_path: str = (
        "data/evaluation/questions.json"
    ),
) -> list[dict]:
    path = Path(dataset_path)

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def evaluate_graph_retrieval(
    dataset_path: str = (
        "data/evaluation/questions.json"
    ),
    max_hops: int = 2,
) -> dict:
    questions = (
        load_evaluation_questions(
            dataset_path
        )
    )

    results = []

    evaluated_questions = 0
    successful_retrievals = 0

    reciprocal_rank_sum = 0.0
    total_latency_ms = 0.0

    for item in questions:
        category = item.get(
            "category",
            "unknown",
        )
        expected_document = (
            item.get(
                "expected_document"
            )
        )

        if expected_document is None:
            continue

        question = item["question"]

        start_time = (
            time.perf_counter()
        )

        graph_result = (
            search_graph_with_evidence(
                question=question,
                max_hops=max_hops,
            )
        )

        latency_ms = (
            time.perf_counter()
            - start_time
        ) * 1000

        total_latency_ms += (
            latency_ms
        )

        retrieved_documents = []

        for chunk in (
            graph_result.evidence_chunks
        ):
            if (
                chunk.title
                not in retrieved_documents
            ):
                retrieved_documents.append(
                    chunk.title
                )

        hit = (
            expected_document
            in retrieved_documents
        )

        reciprocal_rank = 0.0

        if hit:
            successful_retrievals += 1

            rank = (
                retrieved_documents.index(
                    expected_document
                )
                + 1
            )

            reciprocal_rank = (
                1.0 / rank
            )

            reciprocal_rank_sum += (
                reciprocal_rank
            )

        evaluated_questions += 1

        results.append(
            {
                "id": item["id"],
                "category": category,
                "question": question,
                "expected_document": (
                    expected_document
                ),
                "retrieved_documents": (
                    retrieved_documents
                ),
                "relationships_found": len(
                    graph_result.relationships
                ),
                "evidence_chunks_found": len(
                    graph_result.evidence_chunks
                ),
                "hit": hit,
                "reciprocal_rank": (
                    reciprocal_rank
                ),
                "latency_ms": (
                    latency_ms
                ),
            }
        )

    recall = 0.0
    mrr = 0.0
    average_latency_ms = 0.0

    if evaluated_questions > 0:
        recall = (
            successful_retrievals
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
        "max_hops": max_hops,
        "questions_evaluated": (
            evaluated_questions
        ),
        "recall_at_k": recall,
        "mrr": mrr,
        "average_latency_ms": (
            average_latency_ms
        ),
        "results": results,
    }