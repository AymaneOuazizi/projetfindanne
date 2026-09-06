from src.evaluation.retrieval import (
    evaluate_retrieval,
)


def main():
    evaluation = evaluate_retrieval(
        dataset_path=(
            "data/evaluation/questions.json"
        ),
        top_k=3,
    )

    print("\nRetrieval Evaluation")
    print("=" * 50)

    print(
        f"Questions evaluated: "
        f"{evaluation['questions_evaluated']}"
    )

    print(
        f"Recall@{evaluation['top_k']}: "
        f"{evaluation['recall_at_k']:.3f}"
    )

    print(
        f"MRR: "
        f"{evaluation['mrr']:.3f}"
    )

    print("\nDetailed results")
    print("=" * 50)

    for result in evaluation["results"]:
        print(
            f"\n{result['id']}: "
            f"{result['question']}"
        )

        print(
            f"Expected: "
            f"{result['expected_document']}"
        )

        print(
            f"Retrieved: "
            f"{result['retrieved_documents']}"
        )

        print(
            f"Hit: {result['hit']}"
        )

        print(
            f"Rank: {result['rank']}"
        )


if __name__ == "__main__":
    main()