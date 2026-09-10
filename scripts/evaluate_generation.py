from src.evaluation.generation import (
    evaluate_generation,
)


def main():
    evaluation = evaluate_generation(
        dataset_path=(
            "data/evaluation/questions.json"
        ),
        top_k=3,
    )

    print("\nGeneration Evaluation")
    print("=" * 50)

    print(
        "Questions evaluated: "
        f"{evaluation['questions_evaluated']}"
    )

    print(
        "Answerable questions: "
        f"{evaluation['answerable_questions']}"
    )

    print(
        "Unanswerable questions: "
        f"{evaluation['unanswerable_questions']}"
    )

    print(
        "Citation rate: "
        f"{evaluation['citation_rate']:.3f}"
    )

    print(
        "Refusal accuracy: "
        f"{evaluation['refusal_accuracy']:.3f}"
    )

    print("\nDetailed results")
    print("=" * 50)

    for result in evaluation["results"]:
        print(
            f"\n{result['id']}: "
            f"{result['question']}"
        )

        print(
            f"Answer: "
            f"{result['answer']}"
        )

        print(
            f"Citation detected: "
            f"{result['has_citation']}"
        )

        print(
            f"Refusal detected: "
            f"{result['is_refusal']}"
        )

        print(
            f"Correct refusal behavior: "
            f"{result['correct_refusal_behavior']}"
        )

        print(
            f"Retrieved: "
            f"{result['retrieved_sources']}"
        )


if __name__ == "__main__":
    main()