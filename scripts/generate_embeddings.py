from src.embeddings.pipeline import generate_missing_embeddings


def main():
    count = generate_missing_embeddings()

    print(f"Generated embeddings for {count} chunks.")


if __name__ == "__main__":
    main()