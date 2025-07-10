from typing import Annotated

from fastapi import APIRouter, File, Form, UploadFile

from backend.resume_evaluations.exceptions import (
    InvalidResumeFormatError,
)
from backend.resume_evaluations.schemas import (
    ResumeEvaluationResponse,
)
from backend.resume_evaluations.service import evaluate_resume

router = APIRouter(
    prefix="/resume_evaluations",
    tags=["resume_evaluations"],
)


@router.post("/evaluate")
async def evaluate(
    resume_file: Annotated[UploadFile, File(description="Resume PDF file")],
    job_description: Annotated[
        str, Form(min_length=1, description="Job description text")
    ],
) -> ResumeEvaluationResponse:
    """Evaluate a candidate's resume against a job description.

    This endpoint takes a resume PDF file and a job description,
    validates them, and returns structured feedback
    including scores and suggestions.

    Args:
        resume_file (UploadFile): The PDF file containing the resume.
        job_description (str): The job description text (cannot be empty).

    Returns:
        ResumeEvaluationResponse: The evaluation results including scores, verdicts, and feedback.

    """
    # Validate file type
    if (
        resume_file.content_type != "application/pdf"
        or not resume_file.filename
        or not resume_file.filename.lower().endswith(".pdf")
    ):
        raise InvalidResumeFormatError
    return await evaluate_resume(resume_file, job_description)
