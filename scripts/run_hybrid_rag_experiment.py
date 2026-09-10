from src.experiments.hybrid_rag import (
    run_hybrid_rag_experiment,
)


def main():
    results = run_hybrid_rag_experiment(
        dataset_path=(
            "data/evaluation/questions.json"
        ),
        top_k=3,
        candidate_limit=10,
        rrf_k=60,
    )

    retrieval = results["retrieval"]
    generation = results["generation"]

    print("\nHybrid RAG v1")
    print("=" * 50)

    print("\nRetrieval")
    print("-" * 50)

    print(
        f"Recall@3: "
        f"{retrieval['recall_at_k']:.3f}"
    )

    print(
        f"MRR: "
        f"{retrieval['mrr']:.3f}"
    )

    print(
        f"Average latency: "
        f"{retrieval['average_latency_ms']:.2f} ms"
    )

    print("\nGeneration")
    print("-" * 50)

    print(
        f"Citation rate: "
        f"{generation['citation_rate']:.3f}"
    )

    print(
        f"Refusal accuracy: "
        f"{generation['refusal_accuracy']:.3f}"
    )

    print(
        f"Average latency: "
        f"{generation['average_latency_ms']:.2f} ms"
    )


if __name__ == "__main__":
    main()