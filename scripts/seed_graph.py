from src.graph.database import (
    close_neo4j_driver,
)
from src.graph.seed import (
    seed_initial_graph,
)


def main():
    print("\nSeeding SAP Knowledge Graph")
    print("=" * 50)

    try:
        seed_initial_graph()

        print(
            "SAP Knowledge Graph "
            "seeded successfully."
        )

    finally:
        close_neo4j_driver()


if __name__ == "__main__":
    main()