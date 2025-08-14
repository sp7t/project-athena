from typing import Annotated
import os

from fastapi import APIRouter, File, Form, UploadFile, HTTPException

from backend.candidate_comparisons.schemas import CandidateComparisonLLMResponse
from backend.candidate_comparisons.service import compare_candidates
from backend.resume_evaluations.exceptions import InvalidResumeFormatError

router = APIRouter(
    prefix="/candidate-comparisons",
    tags=["Candidate Comparisons"],
)

# Harden env parsing for MAX_RESUMES (default 10)
try:
    _max_resumes = int(os.getenv("ATHENA_COMPARE_MAX_RESUMES", "10"))
except (TypeError, ValueError):
    _max_resumes = 10
MAX_RESUMES = max(1, _max_resumes)


@router.post("/compare", response_model=CandidateComparisonLLMResponse)
async def compare(
    job_description: Annotated[
        str,
        Form(min_length=1, description="Job description text"),
    ],
    resumes: Annotated[
        list[UploadFile],
        File(description="Resume PDF files (.pdf)"),
    ],
) -> CandidateComparisonLLMResponse:
    """Compare multiple uploaded PDF resumes against a job description."""

    # Enforce a hard cap on number of uploads to avoid overwhelming the LLM/API.
    if len(resumes) > MAX_RESUMES:
        raise HTTPException(
            status_code=400,
            detail=f"Too many resumes uploaded ({len(resumes)}). Maximum allowed is {MAX_RESUMES}.",
        )

    # Validate resume formats (PDF only)
    for f in resumes:
        if (
            f.content_type != "application/pdf"
            or not f.filename
            or not f.filename.lower().endswith(".pdf")
        ):
            raise InvalidResumeFormatError

    return await compare_candidates(job_description=job_description, resumes=resumes)
