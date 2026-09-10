import mlflow
from mlflow.tracking import MlflowClient


EXPERIMENT_NAME = "sap-rag-comparison"


def get_latest_run_by_name(
    client: MlflowClient,
    experiment_id: str,
    run_name: str,
):
    runs = client.search_runs(
        experiment_ids=[experiment_id],
        filter_string=(
            f"tags.mlflow.runName = '{run_name}'"
        ),
        order_by=["attributes.start_time DESC"],
        max_results=1,
    )

    if not runs:
        return None

    return runs[0]


def get_metric(
    run,
    metric_name: str,
):
    if run is None:
        return None

    return run.data.metrics.get(metric_name)


def format_metric(
    value,
    decimals: int = 3,
):
    if value is None:
        return "N/A"

    return f"{value:.{decimals}f}"


def main():
    client = MlflowClient()

    experiment = mlflow.get_experiment_by_name(
        EXPERIMENT_NAME
    )

    if experiment is None:
        raise RuntimeError(
            f"Experiment '{EXPERIMENT_NAME}' "
            "was not found."
        )

    vector_run = get_latest_run_by_name(
        client=client,
        experiment_id=experiment.experiment_id,
        run_name="vector_rag_baseline_v1",
    )

    hybrid_run = get_latest_run_by_name(
        client=client,
        experiment_id=experiment.experiment_id,
        run_name="hybrid_rag_v1",
    )

    if vector_run is None:
        raise RuntimeError(
            "Vector RAG run was not found."
        )

    if hybrid_run is None:
        raise RuntimeError(
            "Hybrid RAG run was not found."
        )

    metrics = [
        (
            "Recall@3",
            "retrieval_recall_at_3",
        ),
        (
            "MRR",
            "retrieval_mrr",
        ),
        (
            "Retrieval latency (ms)",
            "retrieval_latency_ms",
        ),
        (
            "Citation rate",
            "citation_rate",
        ),
        (
            "Refusal accuracy",
            "refusal_accuracy",
        ),
        (
            "Generation latency (ms)",
            "generation_latency_ms",
        ),
    ]

    print("\nRAG Architecture Comparison")
    print("=" * 80)

    print(
        f"{'Metric':<30}"
        f"{'Vector RAG':>20}"
        f"{'Hybrid RAG':>20}"
        f"{'Difference':>20}"
    )

    print("-" * 80)

    for label, metric_name in metrics:
        vector_value = get_metric(
            vector_run,
            metric_name,
        )

        hybrid_value = get_metric(
            hybrid_run,
            metric_name,
        )
        difference = (hybrid_value - vector_value)
        if "latency" in metric_name:
            vector_text = format_metric(
                vector_value,
                decimals=2,
            )

            hybrid_text = format_metric(
                hybrid_value,
                decimals=2,
            )
        else:
            vector_text = format_metric(
                vector_value,
                decimals=3,
            )

            hybrid_text = format_metric(
                hybrid_value,
                decimals=3,
            )
        
        print(
            f"{label:<30}"
            f"{vector_text:>20}"
            f"{hybrid_text:>20}"
            f"{difference:>20}"
        )

    print("=" * 80)

    print("\nRuns compared")
    print("-" * 80)

    print(
        "Vector:",
        vector_run.info.run_id,
    )

    print(
        "Hybrid:",
        hybrid_run.info.run_id,
    )


if __name__ == "__main__":
    main()