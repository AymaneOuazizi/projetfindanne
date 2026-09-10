from src.evaluation.graph_generation import (
    evaluate_graph_generation,
)
from src.graph.database import (
    close_neo4j_driver,
)


def main():
    try:
        result = (
            evaluate_graph_generation(
                max_hops=2
            )
        )

        print(
            "\nGraph Generation Evaluation"
        )

        print("=" * 60)

        print(
            "Questions evaluated: "
            f"{result['questions_evaluated']}"
        )

        print(
            "Answerable questions: "
            f"{result['answerable_questions']}"
        )

        print(
            "Unanswerable questions: "
            f"{result['unanswerable_questions']}"
        )

        print(
            "Citation rate: "
            f"{result['citation_rate']:.3f}"
        )

        print(
            "Refusal accuracy: "
            f"{result['refusal_accuracy']:.3f}"
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
                f"Answer: "
                f"{item['answer']}"
            )

            print(
                "Relationships found: "
                f"{item['relationships_found']}"
            )

            print(
                "Evidence chunks: "
                f"{item['evidence_chunks_found']}"
            )

    finally:
        close_neo4j_driver()


if __name__ == "__main__":
    main()