from fastapi import APIRouter

from backend.job_descriptions.schemas import (
    JobDescriptionRequest,
    JobDescriptionResponse,
)
from backend.job_descriptions.service import generate_job_description

router = APIRouter(
    prefix="/job-descriptions",
    tags=["Job Descriptions"],
)


@router.post("/")
async def create_job_description(
    request: JobDescriptionRequest,
) -> JobDescriptionResponse:
    """Generate a job description using LLM based on title, note, key focus, and benefits."""
    description = await generate_job_description(
        job_title=request.title,
        custom_note=request.custom_note,
        key_focus=request.key_focus,
        benefits=request.benefits or "",
    )
    return JobDescriptionResponse(job_description=description)
