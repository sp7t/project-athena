from backend.core.gemini import generate_structured_output

from .exceptions import ResumeEvaluationError
from .prompts import RESUME_EVAL_PROMPT
from .schemas import ResumeEvaluationResponse


async def evaluate_resume(resume_text: str, job_description: str) -> dict:
    """Evaluate resume using Gemini structured output."""
    try:
        prompt = RESUME_EVAL_PROMPT.replace("{resume_text}", resume_text).replace(
            "{job_description}", job_description
        )
        result = await generate_structured_output(prompt, ResumeEvaluationResponse)
        return result.model_dump()  # returns it as a plain dictionary
    except Exception as err:
        raise ResumeEvaluationError(str(err)) from err
