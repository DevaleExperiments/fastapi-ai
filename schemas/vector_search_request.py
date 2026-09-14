from pydantic import BaseModel, Field


class VectorSearchRequest(BaseModel):
    resume_id: int
    top_n: int = Field(default=10, ge=1, le=100)