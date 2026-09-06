from src.ingestion.service import (
    calculate_content_hash,
    split_text,
)


def test_content_hash_is_deterministic():
    text = "SAP document"

    hash_1 = calculate_content_hash(text)
    hash_2 = calculate_content_hash(text)

    assert hash_1 == hash_2


def test_different_content_has_different_hash():
    hash_1 = calculate_content_hash("SAP MM")
    hash_2 = calculate_content_hash("SAP SD")

    assert hash_1 != hash_2


def test_split_text():
    text = "abcdefghij"

    chunks = split_text(
        content=text,
        chunk_size=4,
    )

    assert chunks == [
        "abcd",
        "efgh",
        "ij",
    ]