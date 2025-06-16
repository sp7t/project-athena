from fastapi import APIRouter

from .schemas import ResumeEvaluationRequest, ResumeEvaluationResponse
from .service import evaluate_resume

router = APIRouter(
    tags=["resume_evaluations"],
)


@router.post("/evaluate", response_model=ResumeEvaluationResponse)
def evaluate(payload: ResumeEvaluationRequest) -> ResumeEvaluationResponse:
    """Evaluate a candidate's resume against a job description."""
    return evaluate_resume(payload.resume_text, payload.job_description)
