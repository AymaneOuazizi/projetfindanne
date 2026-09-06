from src.ingestion.pipeline import ingest_directory


def main():
    count = ingest_directory(
        "data/raw/sap"
    )

    print(
        f"\nProcessed {count} documents."
    )


if __name__ == "__main__":
    main()