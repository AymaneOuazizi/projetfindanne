import time

from src.evaluation.generation import (
    has_source_citation,
    is_refusal,
    load_evaluation_dataset,
)
from src.generation.graph_rag import (
    answer_question_graph,
)


def evaluate_graph_generation(
    dataset_path: str = (
        "data/evaluation/questions.json"
    ),
    max_hops: int = 2,
) -> dict:
    questions = (
        load_evaluation_dataset(
            dataset_path
        )
    )

    results = []

    answerable_questions = 0
    unanswerable_questions = 0

    cited_answerable = 0
    correct_refusals = 0

    total_latency_ms = 0.0

    for item in questions:
        question = item["question"]
        category = item.get(
            "category",
            "unknown",
        )
        expected_document = (
            item.get(
                "expected_document"
            )
        )

        start_time = (
            time.perf_counter()
        )

        answer, graph_result = (
            answer_question_graph(
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

        citation_present = (
            has_source_citation(
                answer
            )
        )

        refusal = is_refusal(
            answer
        )

        if expected_document is None:
            unanswerable_questions += 1

            if refusal:
                correct_refusals += 1

        else:
            answerable_questions += 1

            if citation_present:
                cited_answerable += 1

        results.append(
            {
                "id": item["id"],
                "category": category,
                "question": question,
                "expected_document": (
                    expected_document
                ),
                "answer": answer,
                "citation_present": (
                    citation_present
                ),
                "refusal": refusal,
                "relationships_found": len(
                    graph_result.relationships
                ),
                "evidence_chunks_found": len(
                    graph_result.evidence_chunks
                ),
                "latency_ms": (
                    latency_ms
                ),
            }
        )

    citation_rate = 0.0
    refusal_accuracy = 0.0

    if answerable_questions > 0:
        citation_rate = (
            cited_answerable
            / answerable_questions
        )

    if unanswerable_questions > 0:
        refusal_accuracy = (
            correct_refusals
            / unanswerable_questions
        )

    average_latency_ms = 0.0

    if questions:
        average_latency_ms = (
            total_latency_ms
            / len(questions)
        )

    return {
        "questions_evaluated": len(
            questions
        ),
        "answerable_questions": (
            answerable_questions
        ),
        "unanswerable_questions": (
            unanswerable_questions
        ),
        "citation_rate": (
            citation_rate
        ),
        "refusal_accuracy": (
            refusal_accuracy
        ),
        "average_latency_ms": (
            average_latency_ms
        ),
        "results": results,
    }