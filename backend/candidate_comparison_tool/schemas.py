from pydantic import BaseModel, Field

from backend.core.schemas import LLMErrorResponse


class CandidateComparisonRequest(BaseModel):
    """Request model for comparing multiple candidates."""

    job_description: str = Field(
        description="The job description text.",
        examples=["Looking for a Python Developer with strong ML experience."],
    )
    resumes: list[str] = Field(
        description="List of resumes to compare.",
        examples=["Alice's resume text...", "Bob's resume text..."],
    )


class CandidateComparisonResponse(BaseModel):
    """Response model for the comparison result."""

    comparison_summary: str = Field(
        description="The generated comparison summary in markdown."
    )


CandidateComparisonLLMResponse = CandidateComparisonResponse | LLMErrorResponse
