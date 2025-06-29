from pydantic import BaseModel, Field


class InterviewQuestionsRequest(BaseModel):
    """Request model for generating interview questions."""

    job_role: str = Field(
        ...,
        description="The role for which interview questions are being generated.",
        examples=["Frontend Developer"],
    )
    experience_level: str = Field(
        ...,
        description="The experience level of the candidate.",
        examples=["Mid"],
    )
    job_description: str = Field(
        ...,
        description="The detailed job description for the role.",
        examples=[
            "Develop and maintain scalable web applications using React and TypeScript."
        ],
    )


class InterviewQuestionsResponse(BaseModel):
    """Response model for generated interview questions."""

    questions: list[str] = Field(
        ..., description="The list of generated interview questions."
    )
