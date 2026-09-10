import json
from pathlib import Path

import mlflow

from src.config import settings
from src.evaluation.graph_generation import (
    evaluate_graph_generation,
)
from src.evaluation.graph_retrieval import (
    evaluate_graph_retrieval,
)
from src.graph.statistics import (
    get_graph_statistics,
)

EXPERIMENT_NAME = "sap-rag-comparison"
RUN_NAME = "graph_rag_baseline_v1"


def save_json_artifact(
    data: dict,
    path: str,
) -> None:
    file_path = Path(path)

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def run_graph_rag_experiment(
    max_hops: int = 2,
) -> dict:
    mlflow.set_experiment(
        EXPERIMENT_NAME
    )

    print(
        "Running GraphRAG "
        "retrieval evaluation..."
    )

    retrieval_result = (
        evaluate_graph_retrieval(
            max_hops=max_hops
        )
    )

    print(
        "Running GraphRAG "
        "generation evaluation..."
    )

    generation_result = (
        evaluate_graph_generation(
            max_hops=max_hops
        )
    )

    print(
        "Collecting graph statistics..."
    )

    graph_statistics = (
        get_graph_statistics()
    )

    with mlflow.start_run(
        run_name=RUN_NAME
    ) as run:

        # -------------------------
        # Parameters
        # -------------------------

        mlflow.log_param(
            "rag_type",
            "graph",
        )

        mlflow.log_param(
            "graph_database",
            "neo4j",
        )

        mlflow.log_param(
            "max_hops",
            max_hops,
        )

        mlflow.log_param(
            "entity_matching",
            "normalized_exact_match",
        )

        mlflow.log_param(
            "llm_model",
            settings.llm_model,
        )

        mlflow.log_param(
            "chunk_size",
            settings.chunk_size,
        )

        mlflow.log_param(
            "chunk_overlap",
            settings.chunk_overlap,
        )

        # -------------------------
        # Retrieval metrics
        # -------------------------

        mlflow.log_metric(
            "retrieval_recall_at_3",
            retrieval_result[
                "recall_at_k"
            ],
        )

        mlflow.log_metric(
            "retrieval_mrr",
            retrieval_result[
                "mrr"
            ],
        )

        mlflow.log_metric(
            "retrieval_latency_ms",
            retrieval_result[
                "average_latency_ms"
            ],
        )

        # -------------------------
        # Generation metrics
        # -------------------------

        mlflow.log_metric(
            "citation_rate",
            generation_result[
                "citation_rate"
            ],
        )

        mlflow.log_metric(
            "refusal_accuracy",
            generation_result[
                "refusal_accuracy"
            ],
        )

        mlflow.log_metric(
            "generation_latency_ms",
            generation_result[
                "average_latency_ms"
            ],
        )

        # -------------------------
        # Dataset sizes
        # -------------------------

        mlflow.log_metric(
            "retrieval_questions",
            retrieval_result[
                "questions_evaluated"
            ],
        )

        mlflow.log_metric(
            "generation_questions",
            generation_result[
                "questions_evaluated"
            ],
        )

        # -------------------------
        # Graph statistics
        # -------------------------

        mlflow.log_metric(
            "graph_nodes",
            graph_statistics[
                "nodes"
            ],
        )

        mlflow.log_metric(
            "graph_relationships",
            graph_statistics[
                "relationships"
            ],
        )

        # -------------------------
        # Artifacts
        # -------------------------

        retrieval_path = (
            "evaluation/"
            "graph_retrieval_results.json"
        )

        generation_path = (
            "evaluation/"
            "graph_generation_results.json"
        )

        statistics_path = (
            "evaluation/"
            "graph_statistics.json"
        )

        save_json_artifact(
            retrieval_result,
            retrieval_path,
        )

        save_json_artifact(
            generation_result,
            generation_path,
        )

        save_json_artifact(
            graph_statistics,
            statistics_path,
        )

        mlflow.log_artifact(
            retrieval_path,
            artifact_path="evaluation",
        )

        mlflow.log_artifact(
            generation_path,
            artifact_path="evaluation",
        )

        mlflow.log_artifact(
            statistics_path,
            artifact_path="evaluation",
        )

        run_id = run.info.run_id

    return {
        "run_id": run_id,
        "retrieval": retrieval_result,
        "generation": generation_result,
        "graph_statistics": (
            graph_statistics
        ),
    }