from pydantic import BaseModel, Field


class JobDescriptionRequest(BaseModel):
    """Input model for generating a job description."""

    title: str = Field(
        default=...,
        description="The job title (e.g., Data Scientist, Product Manager).",
        examples=["Data Scientist"],
    )
    custom_note: str = Field(
        default=...,
        description="Any custom note like visa requirements or internal comments.",
        examples=["US Citizens only"],
    )
    key_focus: str = Field(
        default=...,
        description="Comma-separated technical and soft skills to emphasize.",
        examples=["Python, SQL, Machine Learning"],
    )
    benefits: str | None = Field(
        default=None,
        description="Optional markdown-formatted list of benefits.",
        examples=["- Remote Flexibility\n- Paid Time Off\n- 401(k)"],
    )


class JobDescriptionResponse(BaseModel):
    """Output model containing the generated job description."""

    job_description: str = Field(
        default=...,
        description="The generated job description in markdown format.",
    )
