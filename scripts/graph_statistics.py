from src.graph.database import (
    close_neo4j_driver,
)
from src.graph.statistics import (
    get_graph_statistics,
)


def main():
    try:
        statistics = (
            get_graph_statistics()
        )

        print(
            "\nKnowledge Graph Statistics"
        )

        print("=" * 60)

        print(
            f"Nodes: "
            f"{statistics['nodes']}"
        )

        print(
            f"Relationships: "
            f"{statistics['relationships']}"
        )

        print("\nNodes by type")
        print("-" * 60)

        for row in statistics["labels"]:
            print(
                f"{row['label']}: "
                f"{row['count']}"
            )

        print(
            "\nRelationships by type"
        )

        print("-" * 60)

        for row in (
            statistics[
                "relationship_types"
            ]
        ):
            print(
                f"{row['type']}: "
                f"{row['count']}"
            )

    finally:
        close_neo4j_driver()


if __name__ == "__main__":
    main()