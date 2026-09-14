from fastapi import APIRouter, Depends, HTTPException

from dependencies.vector_search import get_vector_search_service
from schemas.vector_search_request import VectorSearchRequest
from schemas.vector_search_response import (
    VectorSearchResponse,
    VectorSearchResult,
)
from services.vector_search_service import VectorSearchService


router = APIRouter(
    prefix="/internal/vector",
    tags=["Internal Vector Search"],
)


@router.post(
    "/search",
    response_model=VectorSearchResponse,
)
def search_vectors(
    request: VectorSearchRequest,
    service: VectorSearchService = Depends(
        get_vector_search_service
    ),
):
    results = service.search(
        resume_id=request.resume_id,
        top_n=request.top_n,
    )

    if results is None:
        raise HTTPException(
            status_code=404,
            detail="Resume embedding not found",
        )

    return VectorSearchResponse(
        resume_id=request.resume_id,
        results=[
            VectorSearchResult(
                job_id=job_id,
                similarity=similarity,
            )
            for job_id, similarity in results
        ],
    )