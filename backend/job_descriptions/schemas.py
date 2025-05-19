from pydantic import BaseModel, Field


class JobDescriptionRequest(BaseModel):
    """Request model for generating a job description."""

    title: str = Field(
        ..., description="The title of the job.", example="Software Engineer"
    )
    details: str | None = Field(
        None,
        description="Optional details about the role to include in the description.",
        example="Develop and maintain web applications using Python and React.",
    )


class JobDescriptionResponse(BaseModel):
    """Response model for a generated job description."""

    job_description: str = Field(..., description="The generated job description.")
