from fastapi import FastAPI
from sqlalchemy import text

from src.config import settings
from src.database import engine

from src.api.schemas import (
    SearchRequest,
    SearchResponse,
    SearchResult,
)
from src.retrieval.vector import search_similar_chunks

from src.api.schemas import (
    AskRequest,
    AskResponse,
    SourceResult,
)
from src.generation.rag import answer_question

app = FastAPI(
    title=settings.app_name,
)


@app.get("/")
def root():
    return {
        "message": "SAP RAG Platform API",
        "environment": settings.app_env,
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


@app.get("/health/db")
def database_health():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "healthy",
        "database": "connected",
    }

@app.post(
    "/search",
    response_model=SearchResponse,
)
def semantic_search(
    request: SearchRequest,
) -> SearchResponse:
    results = search_similar_chunks(
        query=request.query,
        limit=request.top_k,
    )

    return SearchResponse(
        query=request.query,
        results=[
            SearchResult(
                chunk_id=result.chunk_id,
                document_id=result.document_id,
                chunk_index=result.chunk_index,
                content=result.content,
                title=result.title,
                source=result.source,
                distance=result.distance,
            )
            for result in results
        ],
    )
@app.post(
    "/ask",
    response_model=AskResponse,
)
def ask_question(
    request: AskRequest,
) -> AskResponse:
    answer, chunks = answer_question(
        question=request.question,
        top_k=request.top_k,
    )

    return AskResponse(
        question=request.question,
        answer=answer,
        sources=[
            SourceResult(
                title=chunk.title,
                source=chunk.source,
                chunk_index=chunk.chunk_index,
                content=chunk.content,
            )
            for chunk in chunks
        ],
    )