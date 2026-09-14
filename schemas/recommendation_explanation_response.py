from pydantic import BaseModel


class RecommendationExplanationResponse(BaseModel):
    explanation: str