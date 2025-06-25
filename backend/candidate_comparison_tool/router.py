from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool

from backend.candidate_comparison_tool.exceptions import GeminiError
from backend.candidate_comparison_tool.schemas import (
    CandidateComparisonLLMResponse,
    CandidateComparisonRequest,
)
from backend.candidate_comparison_tool.service import get_gemini_score

router = APIRouter(
    prefix="/candidate-comparisons",
    tags=["Candidate Comparisons"],
)


@router.post(
    "/compare",
    status_code=200,
)
async def compare_candidates(
    data: CandidateComparisonRequest,
) -> CandidateComparisonLLMResponse:
    """Compare multiple resumes against a job description and return a summary."""
    try:
        return await run_in_threadpool(
            get_gemini_score, data.job_description, data.resumes
        )
    except GeminiError as ge:
        raise HTTPException(status_code=503, detail=str(ge)) from ge
