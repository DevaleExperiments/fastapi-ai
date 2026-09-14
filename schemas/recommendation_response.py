from pydantic import BaseModel


class RecommendationResult(BaseModel):
    job_id: int
    similarity: float


class RecommendationResponse(BaseModel):
    resume_id: int
    recommendations: list[RecommendationResult]