from src.retrieval.bm25 import (
    search_bm25_chunks,
)


def main():
    query = "What is a purchase order?"

    results = search_bm25_chunks(
        query=query,
        limit=3,
    )

    print("\nBM25 Search")
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
            f"BM25 score: "
            f"{result.score:.4f}"
        )

        print(
            f"Content: "
            f"{result.content[:300]}"
        )


if __name__ == "__main__":
    main()