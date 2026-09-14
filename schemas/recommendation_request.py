from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    resume_id: int = Field(gt=0)
    top_n: int = Field(default=10, ge=1, le=100)