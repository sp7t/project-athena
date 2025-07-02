from fastapi import APIRouter

from backend.resume_evaluations.exceptions import (
    MissingJobDescriptionError,
    MissingResumeFileError,
)
from backend.resume_evaluations.schemas import (
    ResumeEvaluationRequest,
    ResumeEvaluationResponse,
)
from backend.resume_evaluations.service import evaluate_resume

router = APIRouter(
    prefix="/resume_evaluations",
    tags=["resume_evaluations"],
)


@router.post("/evaluate")
async def evaluate(request: ResumeEvaluationRequest) -> ResumeEvaluationResponse:
    """Evaluate a candidate's resume against a job description using Gemini LLM.

    This endpoint takes resume text and a job description,
    validates them, and returns structured feedback
    including scores and suggestions.

    Args:
        request (ResumeEvaluationRequest): The input data containing resume and job description.

    Returns:
        ResumeEvaluationResponse: The evaluation results including scores, verdicts, and feedback.

    """
    if not request.resume_text.strip():
        raise MissingResumeFileError

    if not request.job_description.strip():
        raise MissingJobDescriptionError

    return await evaluate_resume(request)
