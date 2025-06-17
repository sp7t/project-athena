from fastapi import APIRouter, FastAPI

from backend.interview_questions.router import router as interview_questions_router
from backend.job_descriptions.router import router as job_descriptions_router

# Add routers to the main API router
router = APIRouter()
router.include_router(job_descriptions_router)
router.include_router(interview_questions_router)
app = FastAPI(
    title="Project Athena",
    description="API endpoints for job description generation and resume evaluations.",
)

app.include_router(router, prefix="/api")
