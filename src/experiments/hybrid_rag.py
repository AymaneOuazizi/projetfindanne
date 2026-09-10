import mlflow

from src.config import settings
from src.evaluation.hybrid_generation import (
    evaluate_hybrid_generation,
)
from src.evaluation.hybrid_retrieval import (
    evaluate_hybrid_retrieval,
)


def run_hybrid_rag_experiment(
    dataset_path: str,
    top_k: int = 3,
    candidate_limit: int = 10,
    rrf_k: int = 60,
) -> dict:
    retrieval_evaluation = (
        evaluate_hybrid_retrieval(
            dataset_path=dataset_path,
            top_k=top_k,
            candidate_limit=candidate_limit,
            rrf_k=rrf_k,
        )
    )

    generation_evaluation = (
        evaluate_hybrid_generation(
            dataset_path=dataset_path,
            top_k=top_k,
            candidate_limit=candidate_limit,
            rrf_k=rrf_k,
        )
    )

    mlflow.set_experiment(
        "sap-rag-comparison"
    )

    with mlflow.start_run(
        run_name="hybrid_rag_v1"
    ):
        mlflow.log_param(
            "rag_type",
            "hybrid",
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

        mlflow.log_param(
            "candidate_limit",
            candidate_limit,
        )

        mlflow.log_param(
            "rrf_k",
            rrf_k,
        )

        mlflow.log_param(
            "llm_model",
            settings.llm_model,
        )

        mlflow.log_metric(
            f"retrieval_recall_at_{top_k}",
            retrieval_evaluation[
                "recall_at_k"
            ],
        )

        mlflow.log_metric(
            "retrieval_mrr",
            retrieval_evaluation[
                "mrr"
            ],
        )

        mlflow.log_metric(
            "retrieval_latency_ms",
            retrieval_evaluation[
                "average_latency_ms"
            ],
        )

        mlflow.log_metric(
            "citation_rate",
            generation_evaluation[
                "citation_rate"
            ],
        )

        mlflow.log_metric(
            "refusal_accuracy",
            generation_evaluation[
                "refusal_accuracy"
            ],
        )

        mlflow.log_metric(
            "generation_latency_ms",
            generation_evaluation[
                "average_latency_ms"
            ],
        )

        mlflow.log_dict(
            retrieval_evaluation,
            "evaluation/retrieval_results.json",
        )

        mlflow.log_dict(
            generation_evaluation,
            "evaluation/generation_results.json",
        )

    return {
        "retrieval": retrieval_evaluation,
        "generation": generation_evaluation,
    }