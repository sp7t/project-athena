from pydantic import BaseModel

from backend.core.schemas import LLMErrorResponse


class CandidateScore(BaseModel):
    """Score breakdown for candidate evaluation categories."""

    Skills_Match: int
    Experience_Relevance: int
    Keyword_Match: int
    Projects: int
    Education: int
    Formatting: int
    Additional_Value: int


class CandidateFeedback(BaseModel):
    """Text feedback for candidate evaluation categories."""

    Skills_Match: str
    Experience_Relevance: str
    Keyword_Match: str
    Projects: str
    Education: str
    Formatting: str
    Additional_Value: str
    Summary: str


class CandidateResult(BaseModel):
    """Individual candidate evaluation result."""

    name: str
    score: CandidateScore
    overall_score: int | None = None
    verdict: str | None = None
    feedback: CandidateFeedback | None = None


class CandidateComparisonResponse(BaseModel):
    """Response containing multiple candidate comparison results."""

    candidates: list[CandidateResult]
    comparison_summary: str


CandidateComparisonLLMResponse = CandidateComparisonResponse | LLMErrorResponse
