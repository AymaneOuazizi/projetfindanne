from src.experiments.graph_rag import (
    run_graph_rag_experiment,
)
from src.graph.database import (
    close_neo4j_driver,
)


def main():
    print(
        "\nGraphRAG MLflow Experiment"
    )

    print("=" * 60)

    try:
        result = (
            run_graph_rag_experiment(
                max_hops=2
            )
        )

        retrieval = (
            result["retrieval"]
        )

        generation = (
            result["generation"]
        )

        graph_statistics = (
            result["graph_statistics"]
        )

        print(
            "\nRetrieval"
        )

        print("-" * 60)

        print(
            "Recall: "
            f"{retrieval['recall_at_k']:.3f}"
        )

        print(
            "MRR: "
            f"{retrieval['mrr']:.3f}"
        )

        print(
            "Latency: "
            f"{retrieval['average_latency_ms']:.2f} ms"
        )

        print(
            "\nGeneration"
        )

        print("-" * 60)

        print(
            "Citation rate: "
            f"{generation['citation_rate']:.3f}"
        )

        print(
            "Refusal accuracy: "
            f"{generation['refusal_accuracy']:.3f}"
        )

        print(
            "Latency: "
            f"{generation['average_latency_ms']:.2f} ms"
        )

        print(
            "\nGraph"
        )

        print("-" * 60)

        print(
            "Nodes: "
            f"{graph_statistics['nodes']}"
        )

        print(
            "Relationships: "
            f"{graph_statistics['relationships']}"
        )

        print(
            "\nMLflow Run ID:"
        )

        print(
            result["run_id"]
        )

    finally:
        close_neo4j_driver()


if __name__ == "__main__":
    main()