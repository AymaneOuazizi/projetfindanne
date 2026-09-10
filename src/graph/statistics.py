from src.config import settings
from src.graph.database import driver


def get_graph_statistics() -> dict:
    with driver.session(
        database=settings.neo4j_database
    ) as session:

        node_count = session.run(
            """
            MATCH (n)
            RETURN count(n) AS count
            """
        ).single()["count"]

        relationship_count = (
            session.run(
                """
                MATCH ()-[r]->()
                RETURN count(r) AS count
                """
            ).single()["count"]
        )

        label_counts = session.run(
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
                    type(r) AS type,
                    count(*) AS count

                ORDER BY type
                """
            ).data()
        )

    return {
        "nodes": node_count,
        "relationships": (
            relationship_count
        ),
        "labels": label_counts,
        "relationship_types": (
            relationship_counts
        ),
    }