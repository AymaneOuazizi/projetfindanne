from fastapi import FastAPI
from sqlalchemy import text

from src.config import settings
from src.database import engine

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