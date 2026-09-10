from src.graph.database import (
    close_neo4j_driver,
)
from src.graph.reset import (
    clear_graph_data,
)


def main():
    print("\nResetting Neo4j graph")
    print("=" * 60)

    try:
        clear_graph_data()

        print(
            "Neo4j graph data cleared "
            "successfully."
        )

    finally:
        close_neo4j_driver()


if __name__ == "__main__":
    main()