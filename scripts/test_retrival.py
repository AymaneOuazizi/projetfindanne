from src.retrieval.vector import search_similar_chunks


def main():
    # query = "What is a purchase order?"
    # query = "What is accounts payable?"
    query = "What does a sales order represent?"

    results = search_similar_chunks(
        query=query,
        limit=3,
    )

    print(f"\nQuestion: {query}\n")

    for result in results:
        print(
            f"Source: {result.title}"
        )
        print(
            f"Distance: {result.distance:.4f}"
        )
        print(result.content)
        print("-" * 60)


if __name__ == "__main__":
    main()