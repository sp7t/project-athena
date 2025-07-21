from pydantic import BaseModel, Field

from backend.core.schemas import LLMErrorResponse


class JobDescriptionRequest(BaseModel):
    """Request model for generating a job description."""

    job_title: str = Field(
        description="The job title (e.g., Data Scientist, Product Manager).",
        examples=["Data Scientist"],
    )
    qualifications: str = Field(
        description="Any qualifications like visa requirements or experience requirements.",
        examples=[
            "US Citizens only",
            "F1 student",
            "OPT",
            "CPT",
            "10+ years of experience",
        ],
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
    custom_note: str | None = Field(
        description=(
            "Any optional note providing additional requirements, niche skills, work eligibility "
            "conditions, or internal preferences to be reflected in the job description."
        ),
        examples=[
            "We are looking for a candidate with a strong background in node.js, python, and SQL.",
            "Candidates with AWS or GCP experience are preferred.",
            "Open to F1, CPT, and OPT applicants.",
            "Ideal for undergrad students looking for internship opportunities.",
            "US Citizens only due to project clearance requirements.",
            "Should be familiar with SOC 2 compliance and ISO 27001 audits.",
            "Internal note: prioritize local candidates if possible.",
            "Looking for someone experienced in medical billing systems.",
            "Visa sponsorship is not available for this role.",
        ],
    )


class JobDescriptionResponse(BaseModel):
    """Response model returned to the client — always contains a job description."""

    job_description: str = Field(
        description="The generated job description in markdown format.",
    )


JobDescriptionLLMResponse = JobDescriptionResponse | LLMErrorResponse
