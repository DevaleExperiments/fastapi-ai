from repositories.job_repository import JobRepository

from schemas.recommendation_response import (
    RecommendationResponse,
    RecommendationResult,
)
from services.ranking_service import RankingService
from services.vector_search_service import VectorSearchService


class RecommendationService:

    def __init__(
        self,
        vector_search_service: VectorSearchService,
        job_repository: JobRepository,
        ranking_service: RankingService,
    ):
        self.vector_search_service = vector_search_service
        self.job_repository = job_repository
        self.ranking_service = ranking_service

    def generate(
        self,
        resume_id: int,
        top_n: int,
    ) -> RecommendationResponse | None:

        results = self.vector_search_service.search(
            resume_id=resume_id,
            top_n=top_n,
        )

        if results is None:
            return None

        ranked_results = self.ranking_service.rank(results)

        job_ids = [
            recommendation.job_id
            for recommendation in ranked_results
        ]

        jobs = self.job_repository.get_by_ids(job_ids)

        jobs_by_id = {
            job.id: job
            for job in jobs
        }

        return RecommendationResponse(
            resume_id=resume_id,
            recommendations=[
                RecommendationResult(
                    job_id=recommendation.job_id,
                    similarity=recommendation.similarity,
                )
                for recommendation in ranked_results
                if recommendation.job_id in jobs_by_id
            ],
        )