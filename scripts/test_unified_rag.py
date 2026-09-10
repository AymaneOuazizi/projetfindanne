from src.generation.unified_rag import (
    ask_rag,
)


def main():
    question = (
        "What is a purchase order?"
    )

    architectures = [
        "vector",
        "hybrid",
        "graph",
    ]

    for architecture in architectures:
        print("\n" + "=" * 60)

        print(
            f"Architecture: "
            f"{architecture}"
        )

        print(
            f"Question: {question}"
        )

        result = ask_rag(
            question=question,
            architecture=architecture,
        )

        print("\nAnswer:")

        print(
            result.answer
        )

        print(
            "\nSources: "
            f"{len(result.sources)}"
        )


if __name__ == "__main__":
    main()