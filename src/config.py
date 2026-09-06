from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SAP RAG Platform"
    app_env: str = "development"

    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    embedding_model: str = (
        "sentence-transformers/"
        "paraphrase-multilingual-MiniLM-L12-v2"
    )
    embedding_dimension: int = 384

    groq_api_key: str | None = None
    llm_model: str = "openai/gpt-oss-120b"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.postgres_user}:"
            f"{self.postgres_password}@"
            f"{self.postgres_host}:"
            f"{self.postgres_port}/"
            f"{self.postgres_db}"
        )


settings = Settings()