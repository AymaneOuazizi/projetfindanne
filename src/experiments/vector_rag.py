import mlflow

from src.config import settings
from src.evaluation.generation import (
    evaluate_generation,
)
from src.evaluation.retrieval import (
    evaluate_retrieval,
)


def run_vector_rag_experiment(
    dataset_path: str,
    top_k: int = 3,
) -> dict:
    retrieval_evaluation = (
        evaluate_retrieval(
            dataset_path=dataset_path,
            top_k=top_k,
        )
    )

    generation_evaluation = (
        evaluate_generation(
            dataset_path=dataset_path,
            top_k=top_k,
        )
    )

    mlflow.set_experiment(
        "sap-rag-comparison"
    )

    with mlflow.start_run(
        run_name="vector_rag_baseline_v1"
    ):
        # ------------------------
        # Architecture
        # ------------------------

        mlflow.log_param(
            "rag_type",
            "vector",
        )

        # ------------------------
        # Embeddings
        # ------------------------

        mlflow.log_param(
            "embedding_model",
            settings.embedding_model,
        )

        mlflow.log_param(
            "embedding_dimension",
            settings.embedding_dimension,
        )

        # ------------------------
        # Chunking
        # ------------------------

        mlflow.log_param(
            "chunk_size",
            settings.chunk_size,
        )

        mlflow.log_param(
            "chunk_overlap",
            settings.chunk_overlap,
        )

        # ------------------------
        # Retrieval
        # ------------------------

        mlflow.log_param(
            "top_k",
            top_k,
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

        # ------------------------
        # Generation
        # ------------------------

        mlflow.log_param(
            "llm_model",
            settings.llm_model,
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

        # ------------------------
        # Dataset information
        # ------------------------

        mlflow.log_metric(
            "retrieval_questions",
            retrieval_evaluation[
                "questions_evaluated"
            ],
        )

        mlflow.log_metric(
            "generation_questions",
            generation_evaluation[
                "questions_evaluated"
            ],
        )

        # ------------------------
        # Detailed artifacts
        # ------------------------

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