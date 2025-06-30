from typing import Literal

from pydantic import BaseModel, EmailStr, Field


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
    title: str = Field(..., description="Job title the candidate applied for.")


class EmailGenerationRequest(BaseModel):
    """Schema representing an email generation request."""

    candidate: CandidateInfo = Field(description="Details of the candidate.")
    verdict: Literal["Yes", "No"] = Field(
        ..., description='Final decision: "Yes" for selected, "No" for rejected.'
    )
    rejection_reason: str | None = Field(
        None, description="Reason for pass or rejection, if applicable."
    )
    notes: str | None = Field(
        None, description="Additional notes to include in the email."
    )


class EmailGenerationResponse(BaseModel):
    """Response model for a generated email."""

    generated_email: str = Field(description="The generated email content.")
