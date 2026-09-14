from fastapi import APIRouter, Depends, HTTPException

from dependencies.resume import get_resume_embedding_service
from dependencies.resume_parsing import get_resume_parsing_service
from services.resume_embedding_service import ResumeEmbeddingService
from services.resume_parsing_service import ResumeParsingService


router = APIRouter(
    prefix="/internal/resumes",
    tags=["Internal Resume AI"],
)


@router.post("/{resume_id}/process")
def process_resume(
    resume_id: int,
    service: ResumeEmbeddingService = Depends(
        get_resume_embedding_service
    ),
):
    embedding = service.generate_and_save(resume_id)

    if embedding is None:
        raise HTTPException(
            status_code=404,
            detail="Resume parsed data not found or has no usable text",
        )

    return {
        "resume_id": resume_id,
        "status": "processed",
    }


@router.post("/{resume_id}/parse")
def parse_resume(
    resume_id: int,
    service: ResumeParsingService = Depends(
        get_resume_parsing_service
    ),
):
    profile = service.parse_and_save(resume_id)

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Resume parsed data not found or has no usable text",
        )

    return profile