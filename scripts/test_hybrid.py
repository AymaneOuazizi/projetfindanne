from src.retrieval.hybrid import (
    search_hybrid_chunks,
)


def main():
    query = "What is a purchase order?"

    results = search_hybrid_chunks(
        query=query,
        limit=3,
        candidate_limit=10,
    )

    print("\nHybrid Search")
    print("=" * 60)

    print(
        f"Query: {query}"
    )

    for index, result in enumerate(
        results,
        start=1,
    ):
        print(
            f"\nResult {index}"
        )

        print(
            f"Document: {result.title}"
        )

        print(
            f"Chunk: {result.chunk_index}"
        )

        print(
            f"RRF score: "
            f"{result.rrf_score:.6f}"
        )

        print(
            f"Content: "
            f"{result.content[:300]}"
        )


if __name__ == "__main__":
    main()