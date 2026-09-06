from src.embeddings.service import embed_text


def test_embedding_dimension():
    embedding = embed_text("SAP procurement")

    assert len(embedding) == 384