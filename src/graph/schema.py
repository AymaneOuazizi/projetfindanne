from src.config import settings
from src.graph.database import driver

SCHEMA_QUERIES = [
    """
    CREATE CONSTRAINT module_entity_id_unique
    IF NOT EXISTS
    FOR (n:Module)
    REQUIRE n.entity_id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT process_entity_id_unique
    IF NOT EXISTS
    FOR (n:Process)
    REQUIRE n.entity_id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT business_object_entity_id_unique
    IF NOT EXISTS
    FOR (n:BusinessObject)
    REQUIRE n.entity_id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT concept_entity_id_unique
    IF NOT EXISTS
    FOR (n:Concept)
    REQUIRE n.entity_id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT document_postgres_id_unique
    IF NOT EXISTS
    FOR (n:Document)
    REQUIRE n.postgres_id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT chunk_postgres_id_unique
    IF NOT EXISTS
    FOR (n:Chunk)
    REQUIRE n.postgres_id IS UNIQUE
    """,

    """
    CREATE INDEX module_name_index
    IF NOT EXISTS
    FOR (n:Module)
    ON (n.name)
    """,

    """
    CREATE INDEX process_name_index
    IF NOT EXISTS
    FOR (n:Process)
    ON (n.name)
    """,

    """
    CREATE INDEX business_object_name_index
    IF NOT EXISTS
    FOR (n:BusinessObject)
    ON (n.name)
    """,

    """
    CREATE INDEX concept_name_index
    IF NOT EXISTS
    FOR (n:Concept)
    ON (n.name)
    """,

    """
    CREATE INDEX document_title_index
    IF NOT EXISTS
    FOR (n:Document)
    ON (n.title)
    """,
]


def initialize_graph_schema() -> None:
    with driver.session(
        database=settings.neo4j_database
    ) as session:
        for query in SCHEMA_QUERIES:
            session.run(query).consume()