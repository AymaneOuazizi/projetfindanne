from src.evaluation.graph_retrieval import (
    evaluate_graph_retrieval,
)
from src.graph.database import (
    close_neo4j_driver,
)


def main():
    try:
        result = (
            evaluate_graph_retrieval(
                max_hops=2
            )
        )

        print(
            "\nGraph Retrieval Evaluation"
        )

        print("=" * 60)

        print(
            "Questions evaluated: "
            f"{result['questions_evaluated']}"
        )

        print(
            "Recall: "
            f"{result['recall_at_k']:.3f}"
        )

        print(
            "MRR: "
            f"{result['mrr']:.3f}"
        )

        print(
            "Average latency: "
            f"{result['average_latency_ms']:.2f} ms"
        )

        print(
            "\nDetailed Results"
        )

        print("=" * 60)

        for item in result["results"]:
            print(
                f"\n{item['id']}: "
                f"{item['question']}"
            )

            print(
                "Expected document: "
                f"{item['expected_document']}"
            )

            print(
                "Retrieved documents: "
                f"{item['retrieved_documents']}"
            )

            print(
                "Relationships found: "
                f"{item['relationships_found']}"
            )

            print(
                "Evidence chunks: "
                f"{item['evidence_chunks_found']}"
            )

            print(
                f"Hit: {item['hit']}"
            )

    finally:
        close_neo4j_driver()


if __name__ == "__main__":
    main()