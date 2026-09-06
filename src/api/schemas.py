from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(
        min_length=3,
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
    )


class SearchResult(BaseModel):
    chunk_id: int
    document_id: int
    chunk_index: int
    content: str
    title: str
    source: str
    distance: float


class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]
    
class AskRequest(BaseModel):
    question: str = Field(
        min_length=3,
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
    )


class SourceResult(BaseModel):
    title: str
    source: str
    chunk_index: int
    content: str


class AskResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceResult]