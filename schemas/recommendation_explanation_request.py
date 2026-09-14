from pydantic import BaseModel, Field


class RecommendationExplanationRequest(BaseModel):
    candidate_profile: str = Field(min_length=1)
    job_title: str = Field(min_length=1)
    company_name: str = Field(min_length=1)
    job_description: str = Field(min_length=1)
    match_score: float = Field(ge=0, le=100)