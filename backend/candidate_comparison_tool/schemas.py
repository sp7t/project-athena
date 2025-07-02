from pydantic import BaseModel, Field

from backend.core.schemas import LLMErrorResponse


class CandidateComparisonRequest(BaseModel):
    """Request model for candidate comparison.

    Attributes
    ----------
    job_description : str
        The job description text.
    resumes : list[str]
        List of resume texts.

    """

    job_description: str = Field(..., description="The job description text.")
    resumes: list[str] = Field(..., description="List of resume texts.")


class CandidateResult(BaseModel):
    """Model representing a candidate's comparison result.

    Attributes
    ----------
    name : str
        The name of the candidate.
    score : dict
        The score or evaluation details for the candidate.

    """

    name: str
    score: dict


class CandidateComparisonResponse(BaseModel):
    """Response model for candidate comparison.

    Attributes
    ----------
    candidates : list[CandidateResult]
        List of candidate comparison results.
    comparison_summary : str
        Summary of the comparison between candidates.

    """

    candidates: list[CandidateResult]
    comparison_summary: str


CandidateComparisonLLMResponse = CandidateComparisonResponse | LLMErrorResponse
