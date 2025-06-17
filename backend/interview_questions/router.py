from fastapi import APIRouter

from backend.interview_questions.exceptions import InterviewQuestionServiceError
from backend.interview_questions.schemas import (
    InterviewQuestionsRequest,
    InterviewQuestionsResponse,
)
from backend.interview_questions.service import generate_interview_questions

router = APIRouter(
    prefix="/interview-questions",
    tags=["Interview Questions"],
)


@router.post("/", response_model=InterviewQuestionsResponse)
async def create_interview_questions(request: InterviewQuestionsRequest):  # noqa: ANN201
    """Generates interview questions based on job role, experience level, and job description."""  # noqa: D401
    try:
        questions = await generate_interview_questions(
            job_role=request.job_role,
            experience_level=request.experience_level,
            job_description=request.job_description,
        )
        return InterviewQuestionsResponse(questions=questions)
    except Exception as e:
        raise InterviewQuestionServiceError(detail=str(e)) from e
