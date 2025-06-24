from pydantic import BaseModel, Field


class JobDescriptionRequest(BaseModel):
    """Request model for generating a job description."""

    job_title: str = Field(
        description="The job title (e.g., Data Scientist, Product Manager).",
        examples=["Data Scientist"],
    )
    custom_note: str = Field(
        description="Any custom note like visa requirements or internal comments.",
        examples=["US Citizens only"],
    )
    key_focus: str = Field(
        description="Comma-separated technical and soft skills to emphasize.",
        examples=["Python, SQL, Machine Learning"],
    )
    benefits: str | None = Field(
        default=None,
        description="Optional markdown-formatted list of benefits.",
        examples=["- Remote Flexibility\n- Paid Time Off\n- 401(k)"],
    )


class JobDescriptionResponse(BaseModel):
    """Response model containing the generated job description."""

    job_description: str = Field(
        description="The generated job description in markdown format.",
    )
