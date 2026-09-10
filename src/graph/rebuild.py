from src.graph.pipeline import (
    run_graph_extraction_pipeline,
)
from src.graph.reset import (
    clear_graph_data,
)
from src.graph.statistics import (
    get_graph_statistics,
)
from src.graph.sync import (
    sync_postgres_to_neo4j,
)


def rebuild_knowledge_graph() -> dict:
    print(
        "1. Clearing existing graph..."
    )

    clear_graph_data()

    print(
        "2. Synchronizing PostgreSQL "
        "documents and chunks..."
    )

    sync_result = (
        sync_postgres_to_neo4j()
    )

    print(
        "3. Extracting entities and "
        "relationships..."
    )

    extraction_result = (
        run_graph_extraction_pipeline()
    )

    print(
        "4. Computing graph statistics..."
    )

    statistics = (
        get_graph_statistics()
    )

    return {
        "sync": sync_result,
        "extraction": extraction_result,
        "statistics": statistics,
    }