from fastapi import FastAPI

from backend.job_descriptions.router import router as jd_router
from backend.resume_evaluations.router import router as re_router

app = FastAPI(title="Project Athena", version="0.1.0")

# mount job-descriptions under /api/job_descriptions
app.include_router(jd_router, prefix="/api/job_descriptions", tags=["job_descriptions"])
# mount resume-evaluations under /api/resume_evaluations
app.include_router(
    re_router, prefix="/api/resume_evaluations", tags=["resume_evaluations"]
)
