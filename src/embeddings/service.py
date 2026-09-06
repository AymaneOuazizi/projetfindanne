from sentence_transformers import SentenceTransformer

from src.config import settings

_model = SentenceTransformer(settings.embedding_model)


def embed_text(text: str) -> list[float]:
    embedding = _model.encode(
        text,
        normalize_embeddings=True,
    )

    return embedding.tolist()


def embed_texts(texts: list[str]) -> list[list[float]]:
    embeddings = _model.encode(
        texts,
        normalize_embeddings=True,
    )

    return embeddings.tolist()