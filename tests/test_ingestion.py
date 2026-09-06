from src.ingestion.service import (
    calculate_content_hash,
    split_text,
)


def test_content_hash_is_deterministic():
    text = "SAP document"

    assert (
        calculate_content_hash(text)
        == calculate_content_hash(text)
    )


def test_different_content_has_different_hash():
    assert (
        calculate_content_hash("SAP MM")
        != calculate_content_hash("SAP SD")
    )


def test_split_text_returns_multiple_chunks():
    text = "SAP procurement process. " * 100

    chunks = split_text(
        content=text,
        chunk_size=200,
        chunk_overlap=50,
    )

    assert len(chunks) > 1
    assert all(len(chunk) > 0 for chunk in chunks)