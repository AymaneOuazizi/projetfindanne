from src.graph.database import (
    close_neo4j_driver,
    verify_neo4j_connection,
)


def main():
    print("\nNeo4j Connection Test")
    print("=" * 50)

    try:
        connected = (
            verify_neo4j_connection()
        )

        if connected:
            print(
                "Neo4j connection: OK"
            )

    finally:
        close_neo4j_driver()


if __name__ == "__main__":
    main()