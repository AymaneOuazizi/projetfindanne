import mlflow

from src.config import settings
from src.evaluation.retrieval import evaluate_retrieval


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
            "questions_evaluated",
            evaluation["questions_evaluated"],
        )

    return evaluation