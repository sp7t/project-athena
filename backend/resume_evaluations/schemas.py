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

    score: float = Field(ge=0, le=100, description="Score between 0 and 100")
    feedback: str = Field(description="Detailed, actionable feedback for this category")


class BaseResumeEvaluation(BaseModel):
    """Base schema for resume evaluation."""

    name: str = Field(description="Candidate's full name")
    experience_years: float = Field(description="Estimated years of experience")
    verdict: EvaluationVerdict = Field(description="Overall fit verdict")
    # Category evaluations
    skills: EvaluationCategory = Field(
        description="Evaluation of the candidate's technical skills"
    )
    experience: EvaluationCategory = Field(
        description="Evaluation of the candidate's relevant work experience"
    )
    keywords: EvaluationCategory = Field(
        description="Evaluation of keyword alignment with the job description"
    )
    projects: EvaluationCategory = Field(
        description="Evaluation of the candidate's project relevance and impact"
    )
    education: EvaluationCategory = Field(
        description="Evaluation of educational background alignment"
    )
    presentation: EvaluationCategory = Field(
        description="Evaluation of resume clarity, structure, and formatting"
    )
    extras: EvaluationCategory = Field(
        description="Evaluation of additional qualifications or extras"
    )
    summary: str = Field(
        description="Concise overall summary highlighting strengths and weaknesses"
    )
    missing_requirements: list[str] = Field(
        description="List of qualifications missing from the resume"
    )
    recommendations: list[str] = Field(
        description="Specific suggestions for improvement"
    )


class ResumeEvaluationResponse(BaseResumeEvaluation):
    """Full JSON response from the resume-evaluation service."""

    overall_score: float = Field(
        ge=0, le=100, description="Calculated weighted overall score between 0 and 100"
    )
