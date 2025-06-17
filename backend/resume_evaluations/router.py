from fastapi import APIRouter

from .schemas import ResumeEvaluationRequest, ResumeEvaluationResponse
from .service import evaluate_resume

router = APIRouter(
    prefix="/resume_evaluations",
    tags=["resume_evaluations"],
)


@router.post("/evaluate")
async def evaluate(payload: ResumeEvaluationRequest) -> ResumeEvaluationResponse:
    """Evaluate a candidate's resume against a job description using Gemini LLM.

    This endpoint takes resume text and a job description,
    passes them to the evaluation service, and returns structured feedback
    including scores and suggestions.

    Args:
        payload (ResumeEvaluationRequest): The input data containing resume and job description.

    Returns:
        ResumeEvaluationResponse: The evaluation results including scores, verdicts, and feedback.

    """
    result = await evaluate_resume(payload.resume_text, payload.job_description)
    return ResumeEvaluationResponse(**result)
