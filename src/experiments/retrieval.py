import json
from pathlib import Path

import mlflow

from src.config import settings
from src.evaluation.retrieval import (
    evaluate_retrieval,
)


def run_vector_retrieval_experiment(
    dataset_path: str,
    top_k: int = 3,
) -> dict:
    evaluation = evaluate_retrieval(
        dataset_path=dataset_path,
        top_k=top_k,
    )

    mlflow.set_experiment(
        "sap-rag-retrieval"
    )

    with mlflow.start_run(
        run_name="vector_rag_baseline_v1"
    ):
        mlflow.log_param(
            "retrieval_type",
            "vector",
        )

        mlflow.log_param(
            "embedding_model",
            settings.embedding_model,
        )

        mlflow.log_param(
            "embedding_dimension",
            settings.embedding_dimension,
        )

        mlflow.log_param(
            "chunk_size",
            settings.chunk_size,
        )

        mlflow.log_param(
            "chunk_overlap",
            settings.chunk_overlap,
        )

        mlflow.log_param(
            "top_k",
            top_k,
        )

        mlflow.log_metric(
            f"recall_at_{top_k}",
            evaluation["recall_at_k"],
        )

        mlflow.log_metric(
            "mrr",
            evaluation["mrr"],
        )

        mlflow.log_metric(
            "average_latency_ms",
            evaluation[
                "average_latency_ms"
            ],
        )

        mlflow.log_metric(
            "questions_evaluated",
            evaluation[
                "questions_evaluated"
            ],
        )

        artifact_path = Path(
            "artifacts"
        )

        artifact_path.mkdir(
            exist_ok=True
        )

        output_file = (
            artifact_path
            / "retrieval_results.json"
        )

        with output_file.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                evaluation,
                file,
                indent=2,
            )

        mlflow.log_artifact(
            str(output_file)
        )

    return evaluation