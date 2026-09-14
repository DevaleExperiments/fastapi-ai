from fastapi import FastAPI

from config import settings
from api.health import router as health_router
from api.resume_ai import router as resume_ai_router
from api.job_ai import router as job_ai_router
from api.vector_search import router as vector_search_router
from api.recommendation_ai import router as recommendation_ai_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(health_router)
app.include_router(resume_ai_router)
app.include_router(job_ai_router)
app.include_router(vector_search_router)
app.include_router(recommendation_ai_router)