from pydantic import BaseModel


class DetailedFeedback(BaseModel):
    """Individual field-level feedback for each scoring category."""

    skills_match_feedback: str
    experience_relevance_feedback: str
    keyword_match_feedback: str
    projects_feedback: str
    education_feedback: str
    formatting_feedback: str
    additional_value_feedback: str


class ResumeEvaluationIn(BaseModel):
    """Request payload for resume evaluation."""

    resume_text: str
    job_description: str


class ResumeEvaluationOut(BaseModel):
    """Full JSON response from the resume-evaluation service."""

    estimated_experience_years: float
    verdict: str
    skills_match: int
    experience_relevance: int
    keyword_match: int
    projects: int
    education: int
    formatting: int
    additional_value: int
    summary_feedback: str
    detailed_feedback: DetailedFeedback
    missing_qualifications: list[str]
    improvement_suggestions: list[str]
