from fastapi import APIRouter

from backend.candidate_comparison_tool.schemas import (
    CandidateComparisonLLMResponse,
    CandidateComparisonRequest,
)
from backend.candidate_comparison_tool.service import compare_candidates

router = APIRouter(
    prefix="/candidate-comparisons",
    tags=["Candidate Comparisons"],
)


@router.post(
    "/compare",
    status_code=200,
)
async def compare(
    payload: CandidateComparisonRequest,
) -> CandidateComparisonLLMResponse:
    """Compare multiple resumes against a job description and return a summary."""
    return await compare_candidates(
        job_description=payload.job_description,
        resumes=payload.resumes,
    )
