from pydantic import BaseModel, Field


class JobDescriptionRequest(BaseModel):
    """Input model for generating a job description."""

    title: str = Field(
        ...,
        description="The job title (e.g., Data Scientist, Product Manager).",
        example="Data Scientist",
    )
    custom_note: str = Field(
        ...,
        description="Any custom note like visa requirements or internal comments.",
        example="US Citizens only",
    )
    key_focus: str = Field(
        ...,
        description="Comma-separated technical and soft skills to emphasize.",
        example="Python, SQL, Machine Learning",
    )
    benefits: str | None = Field(
        None,
        description="Optional markdown-formatted list of benefits.",
        example="- Remote Flexibility\n- Paid Time Off\n- 401(k)",
    )


class JobDescriptionResponse(BaseModel):
    """Output model containing the generated job description."""

    job_description: str = Field(
        ..., description="The generated job description in markdown format."
    )
