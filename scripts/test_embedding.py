from src.embeddings.service import embed_text


def main():
    text = "SAP Materials Management handles procurement."

    vector = embed_text(text)

    print(f"Vector dimension: {len(vector)}")
    print(f"First 5 values: {vector[:5]}")


if __name__ == "__main__":
    main()