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


class Questionanswers(BaseModel):
    """Response model for generated technical interview questions."""

    question: str = Field(..., description="The question for the interview.")
    answer: str = Field(..., description="The answer for the interview.")


class InterviewQuestionsResponse(BaseModel):
    """Response model for generated interview questions."""

    behavioralquestions: list[str] = Field(
        ..., description="The list of generates behavioral interview questions."
    )
    Technicalquestions: list[Questionanswers] = Field(
        ..., description="The list of   generates  technical interview questions."
    )
