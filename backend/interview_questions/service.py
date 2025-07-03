from backend.core.gemini import generate_structured_output
from backend.interview_questions.prompts import INTERVIEW_QUESTIONS_PROMPT
from backend.interview_questions.schemas import (
    InterviewQuestionsRequest,
    InterviewQuestionsResponse,
)


async def generate_interview_questions(
    request: InterviewQuestionsRequest,
) -> InterviewQuestionsResponse:
    """Generate interview questions based on job role, experience level, and optional job description."""
    job_details = f"Role: {request.job_role}\nExperience Level: {request.experience_level}\nJob Description: {request.job_description}"
    prompt = INTERVIEW_QUESTIONS_PROMPT.format(job_details=job_details)
    return await generate_structured_output(prompt, InterviewQuestionsResponse)
