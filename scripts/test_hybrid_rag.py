from src.generation.hybrid_rag import (
    answer_question_hybrid,
)


def main():
    question = "What is a purchase order?"
    # question = "What does a company owe to suppliers?"

    answer, chunks = answer_question_hybrid(
        question=question,
        top_k=3,
        candidate_limit=10,
        rrf_k=60,
    )

    print("\nHybrid RAG")
    print("=" * 60)

    print(
        f"\nQuestion:\n{question}"
    )

    print(
        f"\nAnswer:\n{answer}"
    )

    print("\nRetrieved sources")
    print("-" * 60)

    for index, chunk in enumerate(
        chunks,
        start=1,
    ):
        print(
            f"{index}. "
            f"{chunk.title} "
            f"(chunk {chunk.chunk_index}) "
            f"- RRF: "
            f"{chunk.rrf_score:.6f}"
        )


if __name__ == "__main__":
    main()