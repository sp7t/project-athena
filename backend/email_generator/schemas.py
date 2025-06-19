from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator


class SkillsValidationError(ValueError):
    """Exception raised when no skills are provided for a candidate."""

    def __init__(self) -> None:
        """Initialize the SkillsValidationError with a default message."""
        super().__init__("At least one skill must be provided.")


class CandidateInfo(BaseModel):
    """Schema representing candidate information."""

    name: str = Field(..., description="Full name of the candidate.")
    email: EmailStr = Field(..., description="Email address of the candidate.")
    skills: list[str] = Field(
        ..., description="List of candidate's skills (at least one)."
    )
    experience: str = Field(..., description="Candidate's experience summary.")
    title: str = Field(..., description="Job title the candidate applied for.")

    @field_validator("skills")
    def skills_must_have_at_least_one(cls, v: list[str]) -> list[str]:  # noqa: N805
        """Ensure that the skills list contains at least one skill."""
        if not v or len(v) < 1:
            raise SkillsValidationError
        return v


class EmailRequest(BaseModel):
    """Schema representing an email generation request."""

    candidate: CandidateInfo = Field(..., description="Details of the candidate.")
    verdict: Literal["Yes", "No"] = Field(
        ..., description='Final decision: "Yes" for selected, "No" for rejected.'
    )
    rejection_reason: str | None = Field(
        None, description="Reason for rejection, if applicable."
    )
    notes: str | None = Field(
        None, description="Additional notes to include in the email."
    )


class EmailGenerationResponse(BaseModel):
    """Response model for a generated email."""

    generated_email: str = Field(..., description="The generated email content.")
