from src.graph.extraction import (
    extract_graph_from_text,
)


def main():
    text = """
    SAP MM includes the Procurement process.
    Procurement uses Purchase Requisitions,
    Purchase Orders, and Goods Receipts.

    A Purchase Requisition precedes a
    Purchase Order, and the Purchase Order
    precedes the Goods Receipt.
    """

    print("\nGraph Extraction Test")
    print("=" * 60)

    print("\nInput")
    print("-" * 60)

    print(text.strip())

    extraction = (
        extract_graph_from_text(
            text
        )
    )

    print("\nEntities")
    print("-" * 60)

    for entity in extraction.entities:
        print(
            f"{entity.type:<20} "
            f"{entity.name}"
        )

    print("\nRelationships")
    print("-" * 60)

    for relationship in (
        extraction.relationships
    ):
        print(
            f"{relationship.source} "
            f"--{relationship.type}--> "
            f"{relationship.target}"
        )


if __name__ == "__main__":
    main()