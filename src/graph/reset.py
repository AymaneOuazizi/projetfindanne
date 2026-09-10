from src.config import settings
from src.graph.database import driver


def clear_graph_data() -> None:
    with driver.session(
        database=settings.neo4j_database
    ) as session:
        session.run(
            """
            MATCH (n)
            DETACH DELETE n
            """
        ).consume()