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


class ResumeEvaluationRequest(BaseModel):
    """Request payload for resume evaluation."""

    resume_text: str
    job_description: str


class ResumeEvaluationResponse(BaseModel):
    """Full JSON response from the resume-evaluation service."""

    candidate_name: str  # Full name of the candidate
    estimated_experience_years: float
    verdict: str

    # Each category score is now a float because we scale them
    skills_match: float
    experience_relevance: float
    keyword_match: float
    projects: float
    education: float
    formatting: float
    additional_value: float

    total_score: float  # Total weighted score (0-100)

    summary_feedback: str
    detailed_feedback: DetailedFeedback
    missing_qualifications: list[str]
    improvement_suggestions: list[str]
