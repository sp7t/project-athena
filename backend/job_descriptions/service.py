import json

from backend.core.gemini import generate_text
from backend.job_descriptions.constants import JOB_DESCRIPTION_PROMPT
from backend.job_descriptions.exceptions import (
    InvalidJobRequirementsError,
)
from backend.job_descriptions.utils import extract_json_string


async def generate_job_description(
    job_title: str,
    custom_note: str,
    key_focus: str,
    benefits: str | None,
) -> str:
    """Generate a job description using an LLM based on job title, custom note, key focus, and benefits."""
    prompt = JOB_DESCRIPTION_PROMPT.format(
        job_title=job_title,
        custom_note=custom_note,
        key_focus=key_focus,
        benefits=benefits,
    )

    response_text = await generate_text(prompt)
    json_str = extract_json_string(response_text)
    data = json.loads(json_str)

    if "error" in data:
        raise InvalidJobRequirementsError

    return data["job_description"]
