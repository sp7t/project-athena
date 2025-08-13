from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

SKILLS_EMPTY_MESSAGE = "Skills list must contain at least one non-empty item."


class SkillsValidationError(ValueError):
    """Raised when the skills list is empty or invalid."""


class CandidateInfo(BaseModel):
    """Schema representing candidate information."""

    name: str = Field(..., description="Full name of the candidate.")
    email: EmailStr = Field(..., description="Email address of the candidate.")
    skills: list[str] = Field(
        ..., description="List of candidate's skills (at least one)."
    )
    experience: str = Field(..., description="Candidate's experience summary.")
    job_title: str = Field(
        ..., alias="title", description="Job title the candidate applied for."
    )

    # Trim and validate skills
    @field_validator("skills")
    @classmethod
    def validate_skills_not_empty(cls, v: list[str]) -> list[str]:
        """Validate that skills list contains at least one non-empty item and trim whitespace."""
        # Keep only non-empty strings, trimmed
        cleaned = [s.strip() for s in v if isinstance(s, str) and s.strip()]
        if not cleaned:
            raise SkillsValidationError(SKILLS_EMPTY_MESSAGE)
        return cleaned


class EmailGenerationRequest(BaseModel):
    """Schema representing an email generation request."""

    # allow populating by field name or alias
    model_config = ConfigDict(populate_by_name=True)

    candidate: CandidateInfo = Field(description="Details of the candidate.")
    verdict: Literal["Yes", "No"] = Field(
        ..., description='Final decision: "Yes" for selected, "No" for rejected.'
    )

    # Neutral field name, accept legacy key `rejection_reason`
    reason: str | None = Field(
        default=None,
        alias="rejection_reason",
        description="Optional reason for acceptance or rejection.",
    )

    notes: str | None = Field(
        None, description="Additional notes to include in the email."
    )


class EmailGenerationResponse(BaseModel):
    """Response model for a generated email."""

    generated_email: str = Field(description="The generated email content.")
