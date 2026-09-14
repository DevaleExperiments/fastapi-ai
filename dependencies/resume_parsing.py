from functools import lru_cache

from fastapi import Depends

from sqlalchemy.orm import Session

from config import settings
from providers.llm.local_llm import LocalLLMProvider
from services.resume_experience_service import ResumeExperienceService
from services.resume_parsing_service import ResumeParsingService
from database import get_db
from repositories.resume_parsed_data_repository import ResumeParsedDataRepository

@lru_cache
def get_llm_provider() -> LocalLLMProvider:
    return LocalLLMProvider(
        base_url=settings.llm_base_url,
        model_name=settings.llm_model,
    )


def get_resume_experience_service() -> ResumeExperienceService:
    return ResumeExperienceService()


def get_resume_parsing_service(
    llm_provider: LocalLLMProvider = Depends(get_llm_provider),
    experience_service: ResumeExperienceService = Depends(
        get_resume_experience_service
    ),
) -> ResumeParsingService:
    return ResumeParsingService(
        llm_provider=llm_provider,
        experience_service=experience_service,
    )

def get_resume_parsed_data_repository(
    db: Session = Depends(get_db),
) -> ResumeParsedDataRepository:
    return ResumeParsedDataRepository(db)

def get_resume_parsing_service(
    llm_provider: LocalLLMProvider = Depends(get_llm_provider),
    experience_service: ResumeExperienceService = Depends(
        get_resume_experience_service
    ),
    parsed_data_repository: ResumeParsedDataRepository = Depends(
        get_resume_parsed_data_repository
    ),
) -> ResumeParsingService:
    return ResumeParsingService(
        llm_provider=llm_provider,
        experience_service=experience_service,
        parsed_data_repository=parsed_data_repository,
    )