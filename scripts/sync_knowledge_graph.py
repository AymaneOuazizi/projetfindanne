from src.graph.incremental import (
    sync_knowledge_graph_incrementally,
)


def main():
    print(
        "\nIncremental GraphRAG sync"
    )

    print(
        "=" * 60
    )

    result = (
        sync_knowledge_graph_incrementally()
    )

    print(
        "\nGraph synchronization completed."
    )

    print(
        "=" * 60
    )

    print(
        f"Pending chunks: "
        f"{result['pending_chunks']}"
    )

    print(
        f"Documents synced: "
        f"{result['documents_synced']}"
    )

    print(
        f"Chunks synced: "
        f"{result['chunks_synced']}"
    )

    print(
        f"Chunks processed: "
        f"{result['chunks_processed']}"
    )

    print(
        f"Chunks failed: "
        f"{result['chunks_failed']}"
    )

    print(
        f"Entities extracted: "
        f"{result['entities_extracted']}"
    )

    print(
        f"Relationships extracted: "
        f"{result['relationships_extracted']}"
    )

    print(
        f"Chunks marked processed: "
        f"{result['chunks_marked_processed']}"
    )


if __name__ == "__main__":
    main()