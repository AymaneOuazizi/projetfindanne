from mlflow import MlflowClient

EXPERIMENT_NAME = "sap-rag-comparison"


RUN_NAMES = {
    "Vector": "vector_rag_baseline_v1",
    "Hybrid": "hybrid_rag_v1",
    "Graph": "graph_rag_baseline_v1",
}


METRICS = [
    (
        "Recall",
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


def get_latest_run(
    client: MlflowClient,
    experiment_id: str,
    run_name: str,
):
    runs = client.search_runs(
        experiment_ids=[
            experiment_id
        ],
        filter_string=(
            "tags.mlflow.runName = "
            f"'{run_name}'"
        ),
        order_by=[
            "attributes.start_time DESC"
        ],
        max_results=1,
    )

    if not runs:
        raise RuntimeError(
            "No MLflow run found for "
            f"{run_name}"
        )

    return runs[0]


def format_metric(
    value,
) -> str:
    if value is None:
        return "N/A"

    return f"{value:.3f}"


def main():
    client = MlflowClient()

    experiment = (
        client.get_experiment_by_name(
            EXPERIMENT_NAME
        )
    )

    if experiment is None:
        raise RuntimeError(
            "MLflow experiment not found: "
            f"{EXPERIMENT_NAME}"
        )

    runs = {}

    for architecture, run_name in (
        RUN_NAMES.items()
    ):
        runs[architecture] = (
            get_latest_run(
                client=client,
                experiment_id=(
                    experiment.experiment_id
                ),
                run_name=run_name,
            )
        )

    print(
        "\nRAG Architecture Comparison"
    )

    print("=" * 100)

    print(
        f"{'Metric':<30}"
        f"{'Vector':>20}"
        f"{'Hybrid':>20}"
        f"{'Graph':>20}"
    )

    print("-" * 100)

    for label, metric_name in METRICS:
        values = {}

        for architecture in (
            RUN_NAMES
        ):
            values[architecture] = (
                runs[
                    architecture
                ].data.metrics.get(
                    metric_name
                )
            )

        print(
            f"{label:<30}"
            f"{format_metric(values['Vector']):>20}"
            f"{format_metric(values['Hybrid']):>20}"
            f"{format_metric(values['Graph']):>20}"
        )

    print(
        "\nRun IDs"
    )

    print("-" * 100)

    for architecture in RUN_NAMES:
        print(
            f"{architecture:<10}: "
            f"{runs[architecture].info.run_id}"
        )


if __name__ == "__main__":
    main()