from src.generation.graph_rag import (
    answer_question_graph,
)
from src.graph.database import (
    close_neo4j_driver,
)


def main():
    # question = (
    #     "What business objects are "
    #     "involved in Procurement?"
    # )

    # question = (
    #     "Which SAP module is "
    #     "Purchase Order related to?"
    # )
    question = ("Who founded SAP?")
     
    print(
        "\nGraphRAG Generation Test"
    )

    print("=" * 60)

    print(
        f"Question: {question}"
    )

    try:
        answer, graph_result = (
            answer_question_graph(
                question=question,
                max_hops=2,
            )
        )

        print(
            "\nGraph Relationships"
        )

        print("-" * 60)

        for relation in (
            graph_result.relationships
        ):
            print(
                f"{relation.source_name} "
                f"--{relation.relationship}--> "
                f"{relation.target_name}"
            )

        print(
            "\nEvidence Chunks"
        )

        print("-" * 60)

        for chunk in (
            graph_result.evidence_chunks
        ):
            print(
                f"Chunk {chunk.chunk_id} "
                f"from {chunk.title}"
            )

        print(
            "\nGenerated Answer"
        )

        print("-" * 60)

        print(answer)

    finally:
        close_neo4j_driver()


if __name__ == "__main__":
    main()