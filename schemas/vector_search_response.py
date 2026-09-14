from pydantic import BaseModel


class VectorSearchResult(BaseModel):
    job_id: int
    similarity: float


class VectorSearchResponse(BaseModel):
    resume_id: int
    results: list[VectorSearchResult]