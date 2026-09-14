from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from config import settings
from providers.local_embedding import LocalEmbeddingProvider
from repositories.job_embedding_repository import JobEmbeddingRepository
from repositories.job_repository import JobRepository
from services.job_service import JobService


def get_job_repository(
    db: Session = Depends(get_db),
) -> JobRepository:
    return JobRepository(db)


def get_job_embedding_repository(
    db: Session = Depends(get_db),
) -> JobEmbeddingRepository:
    return JobEmbeddingRepository(db)


@lru_cache
def get_embedding_provider() -> LocalEmbeddingProvider:
    return LocalEmbeddingProvider(settings.embedding_model)


def get_job_service(
    job_repository: JobRepository = Depends(get_job_repository),
    embedding_repository: JobEmbeddingRepository = Depends(
        get_job_embedding_repository
    ),
    embedding_provider: LocalEmbeddingProvider = Depends(
        get_embedding_provider
    ),
) -> JobService:
    return JobService(
        job_repository=job_repository,
        embedding_provider=embedding_provider,
        embedding_repository=embedding_repository,
    )