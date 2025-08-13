from pydantic import BaseModel, Field

from backend.core.schemas import LLMErrorResponse


class CandidateScore(BaseModel):
    """Per-category scores; each must be an integer in [0, 100]."""

    Skills_Match: int = Field(ge=0, le=100)
    Experience_Relevance: int = Field(ge=0, le=100)
    Keyword_Match: int = Field(ge=0, le=100)
    Projects: int = Field(ge=0, le=100)
    Education: int = Field(ge=0, le=100)
    Formatting: int = Field(ge=0, le=100)
    Additional_Value: int = Field(ge=0, le=100)


class CandidateFeedback(BaseModel):
    """Natural-language feedback per category + overall notes."""

    Skills_Match: str
    Experience_Relevance: str
    Keyword_Match: str
    Projects: str
    Education: str
    Formatting: str
    Additional_Value: str
    Summary: str


class CandidateResult(BaseModel):
    """Result for a single candidate."""

    name: str
    score: CandidateScore
    overall_score: int | None = None
    verdict: str | None = None
    feedback: CandidateFeedback | None = None


class CandidateComparisonResponse(BaseModel):
    """Top-level response for comparisons."""

    candidates: list[CandidateResult]
    comparison_summary: str


CandidateComparisonLLMResponse = CandidateComparisonResponse | LLMErrorResponse
