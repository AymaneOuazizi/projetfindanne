from src.graph.database import (
    close_neo4j_driver,
)
from src.graph.provenance import (
    create_entity_provenance,
)


def main():
    print(
        "\nCreating Graph Provenance"
    )

    print("=" * 50)

    try:
        count = (
            create_entity_provenance()
        )

        print(
            "Mappings processed: "
            f"{count}"
        )

        print(
            "Provenance created "
            "successfully."
        )

    finally:
        close_neo4j_driver()


if __name__ == "__main__":
    main()