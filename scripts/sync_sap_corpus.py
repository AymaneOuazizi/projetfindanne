from src.ingestion.corpus_sync import (
    sync_sap_corpus,
)


def main():
    print(
        "\nSynchronizing SAP corpus..."
    )

    print(
        "=" * 60
    )

    result = (
        sync_sap_corpus()
    )

    print(
        "\nSynchronization completed."
    )

    print(
        "=" * 60
    )

    print(
        f"Files found: "
        f"{result['files_found']}"
    )

    print(
        f"Documents processed: "
        f"{result['documents_processed']}"
    )

    print(
        f"Embeddings generated: "
        f"{result['embeddings_generated']}"
    )

    graph_sync = result[
        "graph_sync"
    ]

    if graph_sync is not None:
        print(
            f"Graph pending chunks: "
            f"{graph_sync['pending_chunks']}"
        )

        print(
            f"Graph chunks processed: "
            f"{graph_sync['chunks_processed']}"
        )

        print(
            f"Graph chunks failed: "
            f"{graph_sync['chunks_failed']}"
        )


if __name__ == "__main__":
    main()