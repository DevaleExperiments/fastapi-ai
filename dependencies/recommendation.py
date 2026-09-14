from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from dependencies.vector_search import get_vector_search_service
from repositories.job_repository import JobRepository
from services.ranking_service import RankingService
from services.recommendation_service import RecommendationService
from services.vector_search_service import VectorSearchService


def get_recommendation_service(
    vector_search_service: VectorSearchService = Depends(
        get_vector_search_service
    ),
    db: Session = Depends(get_db),
) -> RecommendationService:
    return RecommendationService(
        vector_search_service=vector_search_service,
        job_repository=JobRepository(db),
        ranking_service=RankingService(),
    )