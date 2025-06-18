from pydantic import BaseModel, Field


class InterviewQuestionsRequest(BaseModel):
    """Request model for generating interview questions."""

    job_role: str = Field(
        ...,
        min_length=1,
        description="The role for which interview questions are being generated.",
        example="Frontend Developer",
    )
    experience_level: str = Field(
        ...,
        min_length=1,
        description="The experience level of the candidate.",
        example="Mid",
    )
    job_description: str = Field(
        ...,
        min_length=1,
        description="The detailed job description for the role.",
        example="Develop and maintain scalable web applications using React and TypeScript.",
    )


class InterviewQuestionsResponse(BaseModel):
    """Response model for generated interview questions."""

    questions: list[str] = Field(
        ..., description="The list of generated interview questions."
    )
