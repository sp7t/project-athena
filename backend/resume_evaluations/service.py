import json

from backend.core.llm import generate_text

from .exceptions import ResumeEvaluationError
from .prompts import RESUME_EVAL_PROMPT


async def evaluate_resume(resume_text: str, job_description: str) -> dict:
    """Call Gemini to evaluate the resume and parse the JSON response."""
    try:
        prompt = RESUME_EVAL_PROMPT.replace("{resume_text}", resume_text).replace(
            "{job_description}", job_description
        )
        raw_response = await generate_text(prompt)

        # Simple fallback: find first '{' and last '}', extract that as JSON
        start = raw_response.find("{")
        end = raw_response.rfind("}") + 1
        if start == -1 or end == -1:
            msg = "Unable to locate JSON object in LLM response"
            raise ResumeEvaluationError(msg)

        json_body = raw_response[start:end]
        return json.loads(json_body)

    except json.JSONDecodeError as err:
        msg = f"JSON parse error: {err}"
        raise ResumeEvaluationError(msg) from err
