from src.graph.database import (
    close_neo4j_driver,
)
from src.graph.retriever import (
    search_graph,
)


def main():
    question = (
        "What business objects are "
        "involved in Procurement?"
    )

    print(
        "\nGraph Retrieval Test"
    )

    print("=" * 60)

    print(
        f"Question: {question}"
    )

    try:
        results = search_graph(
            question
        )

        print("\nRelationships")
        print("-" * 60)

        if not results:
            print(
                "No graph relationships found."
            )

        for result in results:
            print(
                f"{result.source_name} "
                f"--{result.relationship}--> "
                f"{result.target_name}"
            )

            print(
                "Supported by chunks: "
                f"{result.source_chunk_ids}"
            )

    finally:
        close_neo4j_driver()


if __name__ == "__main__":
    main()