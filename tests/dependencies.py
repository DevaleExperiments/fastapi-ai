from fastapi import Depends
from sqlalchemy.orm import Session

from config import settings
from database import get_db

from providers.local_embedding import LocalEmbeddingProvider

from repositories.job_embedding_repository import JobEmbeddingRepository
from repositories.job_repository import JobRepository

from repositories.resume_embedding_repository import ResumeEmbeddingRepository
from repositories.resume_parsed_data_repository import ResumeParsedDataRepository

from services.job_service import JobService
from services.resume_embedding_service import ResumeEmbeddingService


def get_job_repository(
    db: Session = Depends(get_db),
) -> JobRepository:
    return JobRepository(db)


def get_job_embedding_repository(
    db: Session = Depends(get_db),
) -> JobEmbeddingRepository:
    return JobEmbeddingRepository(db)


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


def get_resume_parsed_data_repository(
    db: Session = Depends(get_db),
) -> ResumeParsedDataRepository:
    return ResumeParsedDataRepository(db)


def get_resume_embedding_repository(
    db: Session = Depends(get_db),
) -> ResumeEmbeddingRepository:
    return ResumeEmbeddingRepository(db)


def get_resume_embedding_service(
    parsed_data_repository: ResumeParsedDataRepository = Depends(
        get_resume_parsed_data_repository
    ),
    embedding_repository: ResumeEmbeddingRepository = Depends(
        get_resume_embedding_repository
    ),
    embedding_provider: LocalEmbeddingProvider = Depends(
        get_embedding_provider
    ),
) -> ResumeEmbeddingService:
    return ResumeEmbeddingService(
        parsed_data_repository=parsed_data_repository,
        embedding_repository=embedding_repository,
        embedding_provider=embedding_provider,
        embedding_model=settings.embedding_model,
    )