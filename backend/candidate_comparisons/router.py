from typing import Annotated

from fastapi import APIRouter, File, Form, UploadFile

from backend.candidate_comparisons.schemas import CandidateComparisonLLMResponse
from backend.candidate_comparisons.service import compare_candidates

router = APIRouter(
    prefix="/candidate-comparisons",
    tags=["Candidate Comparisons"],
)


@router.post("/compare")
async def compare(
    job_description: Annotated[str, Form(..., description="Job description text")],
    resumes: Annotated[list[UploadFile], File(..., description="Resume PDF files")],
) -> CandidateComparisonLLMResponse:
    """Compare multiple uploaded PDF resumes against a job description.

    Returns structured scores for each candidate and a summary.
    """
    return await compare_candidates(
        job_description=job_description,
        resumes=resumes,
    )
