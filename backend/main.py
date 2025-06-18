from fastapi import APIRouter, FastAPI

from backend.email_generator.router import router as email_generator_router
from backend.job_descriptions.router import router as job_descriptions_router

# Add routers to the main API router
router = APIRouter()
router.include_router(email_generator_router)
router.include_router(job_descriptions_router)

app = FastAPI(
    title="Project Athena",
    description="API endpoints for job description generation and resume evaluations.",
)

app.include_router(router, prefix="/api")
