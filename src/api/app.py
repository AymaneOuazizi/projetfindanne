from fastapi import FastAPI

from src.config import settings

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