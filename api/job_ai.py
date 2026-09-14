from fastapi import APIRouter, Depends, HTTPException

from dependencies.job import get_job_service
from services.job_service import JobService


router = APIRouter(
    prefix="/internal/jobs",
    tags=["Internal Job AI"],
)


@router.post("/{job_id}/process")
def process_job(
    job_id: int,
    service: JobService = Depends(
        get_job_service
    ),
):
    embedding = service.generate_and_save_embedding(job_id)

    if embedding is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return {
        "job_id": job_id,
        "status": "processed",
    }