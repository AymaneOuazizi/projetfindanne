from src.graph.database import (
    close_neo4j_driver,
)
from src.graph.rebuild import (
    rebuild_knowledge_graph,
)


def main():
    print(
        "\nRebuilding SAP "
        "Knowledge Graph"
    )

    print("=" * 60)

    try:
        result = (
            rebuild_knowledge_graph()
        )

        print(
            "\nRebuild completed."
        )

        print("=" * 60)

        sync_result = result["sync"]

        print(
            "Documents synchronized: "
            f"{sync_result['documents']}"
        )

        print(
            "Chunks synchronized: "
            f"{sync_result['chunks']}"
        )

        extraction = (
            result["extraction"]
        )

        print(
            "Chunks processed: "
            f"{extraction['chunks_processed']}"
        )

        print(
            "Chunks failed: "
            f"{extraction['chunks_failed']}"
        )

        print(
            "Entities extracted: "
            f"{extraction['entities_extracted']}"
        )

        print(
            "Relationships extracted: "
            f"{extraction['relationships_extracted']}"
        )

        statistics = (
            result["statistics"]
        )

        print(
            "Graph nodes: "
            f"{statistics['nodes']}"
        )

        print(
            "Graph relationships: "
            f"{statistics['relationships']}"
        )

    finally:
        close_neo4j_driver()


if __name__ == "__main__":
    main()