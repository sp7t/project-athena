from fastapi import APIRouter, FastAPI

from backend.job_descriptions.router import router as job_descriptions_router
from backend.resume_evaluations.router import router as resume_evaluations_router

router = APIRouter()
router.include_router(job_descriptions_router)
router.include_router(resume_evaluations_router)

app = FastAPI(
    title="Project Athena",
    description="API endpoints for job description generation and resume evaluations.",
)

app.include_router(router, prefix="/api")
