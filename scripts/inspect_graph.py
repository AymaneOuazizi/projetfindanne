from src.config import settings
from src.graph.database import (
    close_neo4j_driver,
    driver,
)


def main():
    try:
        with driver.session(
            database=settings.neo4j_database
        ) as session:

            node_counts = session.run(
                """
                MATCH (n)

                UNWIND labels(n) AS label

                RETURN
                    label,
                    count(*) AS count

                ORDER BY label
                """
            ).data()

            relationship_counts = (
                session.run(
                    """
                    MATCH ()-[r]->()

                    RETURN
                        type(r) AS relationship,
                        count(*) AS count

                    ORDER BY relationship
                    """
                ).data()
            )

            relationships = session.run(
                """
                MATCH (source)-[r]->(target)

                RETURN
                    source.name AS source,
                    type(r) AS relationship,
                    target.name AS target

                ORDER BY
                    source,
                    relationship,
                    target
                """
            ).data()

            print("\nNode Counts")
            print("=" * 60)

            for row in node_counts:
                print(
                    f"{row['label']}: "
                    f"{row['count']}"
                )

            print("\nRelationship Counts")
            print("=" * 60)

            for row in relationship_counts:
                print(
                    f"{row['relationship']}: "
                    f"{row['count']}"
                )

            print("\nRelationships")
            print("=" * 60)

            for row in relationships:
                print(
                    f"{row['source']} "
                    f"--{row['relationship']}--> "
                    f"{row['target']}"
                )

    finally:
        close_neo4j_driver()


if __name__ == "__main__":
    main()