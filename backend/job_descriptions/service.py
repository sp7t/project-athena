import json
import re
from json import JSONDecodeError
from typing import Never

from backend.core.llm import generate_text
from backend.job_descriptions.constants import JOB_DESCRIPTION_PROMPT
from backend.job_descriptions.exceptions import (
    InvalidJobRequirementsError,
    raise_service_error,
)


def extract_json_string(text: str) -> str:
    """Extract JSON object from the LLM response, removing markdown code fences if present."""
    code_fence_pattern = r"```(?:json)?\s*(\{.*?\})\s*```"
    match = re.search(code_fence_pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


def raise_invalid_input_error(message: str) -> Never:
    """Raise InvalidJobInputError with the given message."""
    raise InvalidJobRequirementsError(detail=message)


async def generate_job_description(
    job_title: str,
    custom_note: str,
    key_focus: str,
    benefits: str = "",
) -> str:
    """Generate a job description using an LLM based on job title, custom note, key focus, and benefits."""
    try:
        prompt = JOB_DESCRIPTION_PROMPT.format(
            job_title=job_title,
            custom_note=custom_note,
            key_focus=key_focus,
            benefits=benefits,
        )

        response_text = await generate_text(prompt)
        json_str = extract_json_string(response_text)

        try:
            data = json.loads(json_str)
        except JSONDecodeError as e:
            raise_service_error(
                "The language model returned invalid JSON. Please try again.", e
            )

        if "error" in data:
            raise_invalid_input_error(data["error"])

        return data["job_description"]

    except InvalidJobRequirementsError:
        raise
    except JSONDecodeError as e:
        raise_service_error(
            "An unexpected error occurred during job description generation.", e
        )
