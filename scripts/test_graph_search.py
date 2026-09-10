from src.graph.database import (
    close_neo4j_driver,
)
from src.graph.search import (
    search_graph_with_evidence,
)


def main():
    # question = (
    #     "What business objects are "
    #     "involved in Procurement?"
    # )
    question = (
        "What is Purchase Order "
        "related to?"
    )
    print(
        "\nGraph Search with Evidence"
    )

    print("=" * 60)

    print(
        f"Question: {question}"
    )

    try:
        result = (
            search_graph_with_evidence(
                question=question,
                max_hops=2,
            )
        )

        print(
            "\nGraph Relationships"
        )

        print("-" * 60)

        if not result.relationships:
            print(
                "No relationships found."
            )

        for relation in (
            result.relationships
        ):
            print(
                f"{relation.source_name} "
                f"--{relation.relationship}--> "
                f"{relation.target_name}"
            )

            print(
                f"Direction: "
                f"{relation.direction}"
            )

            print(
                "Source chunks: "
                f"{relation.source_chunk_ids}"
            )

            print()

        print("\nEvidence Chunks")
        print("-" * 60)

        if not result.evidence_chunks:
            print(
                "No evidence chunks found."
            )

        for chunk in (
            result.evidence_chunks
        ):
            print(
                f"\nChunk ID: "
                f"{chunk.chunk_id}"
            )

            print(
                f"Document: "
                f"{chunk.title}"
            )

            print(
                f"Chunk index: "
                f"{chunk.chunk_index}"
            )

            print("\nContent:")

            print(
                chunk.content
            )

            print(
                "\n"
                + "-" * 60
            )

    finally:
        close_neo4j_driver()


if __name__ == "__main__":
    main()