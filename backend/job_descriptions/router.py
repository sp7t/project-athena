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
    """
    Generates a job description using a language model based on the provided job title, custom note, key focus areas, and benefits.
    
    Parameters:
        request (JobDescriptionRequest): Contains the job title, custom note, key focus, and benefits for generating the job description.
    
    Returns:
        JobDescriptionResponse: The generated job description.
    """
    return await generate_job_description(
        job_title=request.job_title,
        custom_note=request.custom_note,
        key_focus=request.key_focus,
        benefits=request.benefits,
    )
