from fastapi import APIRouter, FastAPI

from backend.candidate_comparison_tool.router import (
    router as candidate_comparison_router,
)
from backend.job_descriptions.router import router as job_descriptions_router

api_router = APIRouter()
api_router.include_router(job_descriptions_router)
api_router.include_router(candidate_comparison_router)

app = FastAPI(
    title="Project Athena",
    description="API endpoints for job description generation, resume evaluations, and candidate comparisons.",
)

app.include_router(api_router, prefix="/api")
