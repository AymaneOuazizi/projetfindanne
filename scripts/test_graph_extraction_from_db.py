from src.database import SessionLocal
from src.graph.extraction import (
    extract_graph_from_text,
)
from src.models.chunk import Chunk
from src.models.document import Document


def main():
    with SessionLocal() as session:
        row = (
            session.query(
                Chunk,
                Document,
            )
            .join(
                Document,
                Chunk.document_id
                == Document.id,
            )
            .filter(
                Document.title
                == "sap_mm"
            )
            .order_by(
                Chunk.chunk_index
            )
            .first()
        )

        if row is None:
            raise RuntimeError(
                "No sap_mm chunk found."
            )

        chunk, document = row

        print(
            "\nGraph Extraction "
            "from PostgreSQL"
        )

        print("=" * 60)

        print(
            f"Document: "
            f"{document.title}"
        )

        print(
            f"Chunk ID: "
            f"{chunk.id}"
        )

        print(
            f"Chunk index: "
            f"{chunk.chunk_index}"
        )

        print("\nContent")
        print("-" * 60)

        print(
            chunk.content
        )

        extraction = (
            extract_graph_from_text(
                chunk.content
            )
        )

        print("\nEntities")
        print("-" * 60)

        for entity in (
            extraction.entities
        ):
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