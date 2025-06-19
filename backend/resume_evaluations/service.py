import json

from backend.core.llm import generate_text

from .exceptions import ResumeEvaluationError
from .prompts import RESUME_EVAL_PROMPT


async def evaluate_resume(resume_text: str, job_description: str) -> dict:
    """Call Gemini to evaluate the resume and parse the JSON response."""
    prompt = RESUME_EVAL_PROMPT.format(
        resume_text=resume_text,
        job_description=job_description,
    )
    try:
        raw = await generate_text(prompt)
        body = raw[raw.find("{") : raw.rfind("}") + 1]
        return json.loads(body)
    except json.JSONDecodeError as err:
        msg = f"JSON parse error: {err}"
        raise ResumeEvaluationError(msg) from err
