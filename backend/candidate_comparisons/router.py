from typing import Annotated

from fastapi import APIRouter, File, Form, UploadFile

from backend.candidate_comparisons.schemas import CandidateComparisonLLMResponse
from backend.candidate_comparisons.service import compare_candidates
from backend.resume_evaluations.exceptions import InvalidResumeFormatError

router = APIRouter(
    prefix="/candidate-comparisons",
    tags=["Candidate Comparisons"],
)


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
    """Compare multiple uploaded PDF resumes against a job description.

    Returns structured scores for each candidate and a summary.
    """
    # Validate resume formats
    for f in resumes:
        if (
            f.content_type != "application/pdf"
            or not f.filename
            or not f.filename.lower().endswith(".pdf")
        ):
            raise InvalidResumeFormatError

    return await compare_candidates(
        job_description=job_description,
        resumes=resumes,
    )
