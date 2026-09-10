from src.graph.database import (
    close_neo4j_driver,
)
from src.graph.pipeline import (
    run_graph_extraction_pipeline,
)


def main():
    print(
        "\nAutomatic Knowledge "
        "Graph Construction"
    )

    print("=" * 60)

    try:
        result = (
            run_graph_extraction_pipeline()
        )

        print(
            "\nSummary"
        )

        print("-" * 60)

        print(
            "Chunks total: "
            f"{result['chunks_total']}"
        )

        print(
            "Chunks processed: "
            f"{result['chunks_processed']}"
        )

        print(
            "Chunks failed: "
            f"{result['chunks_failed']}"
        )

        print(
            "Entities extracted: "
            f"{result['entities_extracted']}"
        )

        print(
            "Relationships extracted: "
            f"{result['relationships_extracted']}"
        )

        print(
            "\nDetailed results"
        )

        print("-" * 60)

        for item in result["results"]:
            print(
                f"\nDocument: "
                f"{item['document_title']}"
            )

            print(
                f"Chunk: "
                f"{item['chunk_id']}"
            )

            print(
                f"Status: "
                f"{item['status']}"
            )

            if (
                item["status"]
                == "success"
            ):
                print(
                    "Entities: "
                    f"{item['entities_extracted']}"
                )

                print(
                    "Relationships: "
                    f"{item['relationships_extracted']}"
                )

            else:
                print(
                    "Error: "
                    f"{item['error']}"
                )

    finally:
        close_neo4j_driver()


if __name__ == "__main__":
    main()