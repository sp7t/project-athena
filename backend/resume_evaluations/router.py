from fastapi import APIRouter, HTTPException

from .exceptions import ResumeEvaluationError
from .schemas import ResumeEvaluationIn, ResumeEvaluationOut
from .service import evaluate_resume

router = APIRouter(
    tags=["resume_evaluations"],
)


@router.post("/evaluate")
def evaluate(payload: ResumeEvaluationIn) -> ResumeEvaluationOut:
    """Evaluate a candidate"s resume against a job description."""
    try:
        return evaluate_resume(payload.resume_text, payload.job_description)
    except ResumeEvaluationError as err:
        # preserve the original traceback
        raise HTTPException(status_code=500, detail=str(err)) from err
