from src.graph.database import (
    close_neo4j_driver,
)
from src.graph.entity_search import (
    find_entities_in_question,
)


def main():
    question = (
        "What happens after a "
        "Purchase Requisition?"
    )

    print(
        "\nGraph Entity Search"
    )

    print("=" * 60)

    print(
        f"Question: {question}"
    )

    try:
        matches = (
            find_entities_in_question(
                question
            )
        )

        print("\nMatches")
        print("-" * 60)

        if not matches:
            print(
                "No entities found."
            )

        for match in matches:
            print(
                f"{match.label:<20} "
                f"{match.name:<30} "
                f"{match.entity_id}"
            )

    finally:
        close_neo4j_driver()


if __name__ == "__main__":
    main()