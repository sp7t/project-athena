from fastapi import APIRouter

from backend.job_descriptions.exceptions import JobDescriptionServiceError
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
    """Receives job title and details, generates a job description using an LLM."""
    try:
        generated_description = await generate_job_description(
            title=request.title, details=request.details
        )
        return JobDescriptionResponse(job_description=generated_description)
    except Exception as e:
        raise JobDescriptionServiceError(detail=str(e)) from e
