from fastapi import APIRouter

from backend.interview_questions.schemas import (
    InterviewQuestionsRequest,
    InterviewQuestionsResponse,
)
from backend.interview_questions.service import generate_interview_questions

router = APIRouter(
    prefix="/interview-questions",
    tags=["Interview Questions"],
)


@router.post("/")
async def create_interview_questions(
    request: InterviewQuestionsRequest,
) -> InterviewQuestionsResponse:
    """Generate interview questions based on job role, experience level, and job description."""
    return await generate_interview_questions(request)
