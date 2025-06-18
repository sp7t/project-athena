import json
import re

from backend.core.llm import generate_text

from .exceptions import ResumeEvaluationError
from .prompts import RESUME_EVAL_PROMPT


async def evaluate_resume(resume_text: str, job_description: str) -> dict:
    """Call Gemini to evaluate the resume and parse the JSON response."""
    try:
        # Safer string replacement instead of .format() to avoid brace conflicts
        prompt = RESUME_EVAL_PROMPT.replace("{resume_text}", resume_text).replace(
            "{job_description}", job_description
        )

        raw_response = await generate_text(prompt)

        # Search for the outermost JSON object
        match = re.search(r"\{(?:[^{}]|(?R))*\}", raw_response, re.DOTALL)
        if not match:
            msg = "Unable to locate JSON object in LLM response"
            raise ResumeEvaluationError(msg)  # noqa: TRY301

        return json.loads(match.group(0))

    except json.JSONDecodeError as err:
        msg = f"JSON parse error: {err}"
        raise ResumeEvaluationError(msg) from err
    except Exception as err:
        msg = f"Resume evaluation failed: {err}"
        raise ResumeEvaluationError(msg) from err
