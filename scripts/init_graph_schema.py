from src.graph.database import (
    close_neo4j_driver,
)
from src.graph.schema import (
    initialize_graph_schema,
)


def main():
    print("\nInitializing Neo4j schema")
    print("=" * 50)

    try:
        initialize_graph_schema()

        print(
            "Neo4j schema initialized successfully."
        )

    finally:
        close_neo4j_driver()


if __name__ == "__main__":
    main()