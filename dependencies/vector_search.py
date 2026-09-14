from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from repositories.job_embedding_repository import JobEmbeddingRepository
from repositories.resume_embedding_repository import ResumeEmbeddingRepository
from services.vector_search_service import VectorSearchService


def get_vector_search_service(
    db: Session = Depends(get_db),
) -> VectorSearchService:
    return VectorSearchService(
        resume_embedding_repository=ResumeEmbeddingRepository(db),
        job_embedding_repository=JobEmbeddingRepository(db),
    )