from neo4j import GraphDatabase

from src.config import settings


driver = GraphDatabase.driver(
    settings.neo4j_uri,
    auth=(
        settings.neo4j_user,
        settings.neo4j_password,
    ),
)


def verify_neo4j_connection() -> bool:
    driver.verify_connectivity()

    return True


def close_neo4j_driver() -> None:
    driver.close()