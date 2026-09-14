from fastapi import APIRouter, Depends

from dependencies.llm_service import get_llm_service
from schemas.recommendation_explanation_request import (
    RecommendationExplanationRequest,
)
from schemas.recommendation_explanation_response import (
    RecommendationExplanationResponse,
)
from services.llm_service import JobExplanationContext, LLMService

from fastapi import APIRouter, Depends, HTTPException

from dependencies.llm_service import get_llm_service
from dependencies.recommendation import get_recommendation_service

from schemas.recommendation_explanation_request import (
    RecommendationExplanationRequest,
)
from schemas.recommendation_explanation_response import (
    RecommendationExplanationResponse,
)
from schemas.recommendation_request import RecommendationRequest
from schemas.recommendation_response import RecommendationResponse

from services.llm_service import JobExplanationContext, LLMService
from services.recommendation_service import RecommendationService

router = APIRouter(
    prefix="/internal/recommendations",
    tags=["Internal Recommendation AI"],
)


@router.post(
    "/explain",
    response_model=RecommendationExplanationResponse,
)
def explain_recommendation(
    request: RecommendationExplanationRequest,
    service: LLMService = Depends(
        get_llm_service
    ),
):
    context = JobExplanationContext(
        candidate_profile=request.candidate_profile,
        job_title=request.job_title,
        company_name=request.company_name,
        job_description=request.job_description,
        match_score=request.match_score,
    )

    explanation = service.generate_job_explanation(
        context
    )

    return RecommendationExplanationResponse(
        explanation=explanation,
    )

@router.post(
    "/generate",
    response_model=RecommendationResponse,
)
def generate_recommendations(
    request: RecommendationRequest,
    service: RecommendationService = Depends(
        get_recommendation_service
    ),
):
    recommendations = service.generate(
        resume_id=request.resume_id,
        top_n=request.top_n,
    )

    if recommendations is None:
        raise HTTPException(
            status_code=404,
            detail="Resume embedding not found",
        )

    return recommendations