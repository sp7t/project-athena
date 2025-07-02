from fastapi import APIRouter, HTTPException

from backend.candidate_comparison_tool.schemas import (
    CandidateComparisonLLMResponse,
    CandidateComparisonRequest,
)
from backend.candidate_comparison_tool.service import compare_candidates
from backend.resume_evaluations.exceptions import ResumeEvaluationError

router = APIRouter(
    prefix="/candidate-comparisons",
    tags=["Candidate Comparisons"],
)


@router.post(
    "/compare",
)
async def compare_candidates_route(
    payload: CandidateComparisonRequest,
) -> CandidateComparisonLLMResponse:
    """Compare multiple resumes by reusing resume evaluation."""
    try:
        result = await compare_candidates(
            job_description=payload.job_description,
            resumes=payload.resumes,
        )
    except ResumeEvaluationError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    else:
        return result
