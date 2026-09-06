from src.experiments.retrieval import (
    run_vector_retrieval_experiment,
)


def main():
    evaluation = (
        run_vector_retrieval_experiment(
            dataset_path=(
                "data/evaluation/questions.json"
            ),
            top_k=3,
        )
    )

    print("\nExperiment completed")
    print("=" * 50)

    print(
        f"Recall@3: "
        f"{evaluation['recall_at_k']:.3f}"
    )

    print(
        f"MRR: "
        f"{evaluation['mrr']:.3f}"
    )


if __name__ == "__main__":
    main()