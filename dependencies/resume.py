from fastapi import Depends
from sqlalchemy.orm import Session

from config import settings
from database import get_db
from dependencies.job import get_embedding_provider
from providers.local_embedding import LocalEmbeddingProvider
from repositories.resume_embedding_repository import ResumeEmbeddingRepository
from repositories.resume_parsed_data_repository import ResumeParsedDataRepository
from services.resume_embedding_service import ResumeEmbeddingService


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