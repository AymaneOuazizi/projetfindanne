from src.graph.database import (
    close_neo4j_driver,
)
from src.graph.sync import (
    sync_postgres_to_neo4j,
)


def main():
    print(
        "\nPostgreSQL -> Neo4j Sync"
    )

    print("=" * 50)

    try:
        result = (
            sync_postgres_to_neo4j()
        )

        print(
            "Documents synchronized: "
            f"{result['documents']}"
        )

        print(
            "Chunks synchronized: "
            f"{result['chunks']}"
        )

        print(
            "\nSynchronization "
            "completed successfully."
        )

    finally:
        close_neo4j_driver()


if __name__ == "__main__":
    main()