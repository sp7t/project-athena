from enum import Enum

from pydantic import BaseModel, Field


class EvaluationVerdict(str, Enum):
    """Possible evaluation verdicts for resume assessment."""

    STRONG_MATCH = "Strong Match"
    GOOD_MATCH = "Good Match"
    PARTIAL_MATCH = "Partial Match"
    WEAK_MATCH = "Weak Match"
    NOT_RECOMMENDED = "Not Recommended"


class EvaluationCategory(BaseModel):
    """Score and feedback for a single evaluation category."""

    score: float = Field(ge=0, le=100, description="...")
    feedback: str = Field(description="...")


class BaseResumeEvaluation(BaseModel):
    """Base schema for resume evaluation."""

    name: str = Field(description="...")
    experience_years: float = Field(description="...")
    verdict: EvaluationVerdict = Field(description="...")
    # Category evaluations
    skills: EvaluationCategory = Field(description="...")
    experience: EvaluationCategory = Field(description="...")
    keywords: EvaluationCategory = Field(description="...")
    projects: EvaluationCategory = Field(description="...")
    education: EvaluationCategory = Field(description="...")
    presentation: EvaluationCategory = Field(description="...")
    extras: EvaluationCategory = Field(description="...")
    summary: str = Field(description="...")
    missing_requirements: list[str] = Field(description="...")
    recommendations: list[str] = Field(description="...")


class ResumeEvaluationResponse(BaseResumeEvaluation):
    """Full JSON response from the resume-evaluation service."""

    overall_score: float = Field(ge=0, le=100, description="...")
