import re

from backend.core.gemini import generate_text
from backend.interview_questions.prompts import INTERVIEW_QUESTION_PROMPT


async def generate_interview_questions(
    job_role: str, experience_level: str, job_description: str | None
) -> list[str]:
    """Generate interview questions based on job role, experience level, and optional job description.

    Args:
        job_role (str): The job role for which to generate questions.
        experience_level (str): The experience level of the candidate.
        job_description (str | None): Optional job description to provide more context.

    Returns:
        list[str]: A list of generated interview questions.

    """
    job_desc_section = (
        f"\nJob Description:\n{job_description}" if job_description else ""
    )
    prompt = INTERVIEW_QUESTION_PROMPT.format(
        job_role=job_role,
        experience_level=experience_level,
        job_description_section=job_desc_section,
    )
    generated = await generate_text(prompt)
    # Split into a list of questions (handles Q1:, Q2:, etc.)
    questions = re.split("\n(?=Q\\d+:)", generated.strip())
    # Remove empty strings and strip whitespace
    return [q.strip() for q in questions if q.strip()]
