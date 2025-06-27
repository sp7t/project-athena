from backend.core.gemini import generate_structured_output
from backend.core.schemas import LLMErrorResponse
from backend.job_descriptions.constants import JOB_DESCRIPTION_PROMPT
from backend.job_descriptions.exceptions import (
    InvalidJobRequirementsError,
)
from backend.job_descriptions.schemas import (
    JobDescriptionResponse,
    JobDescriptionResult,
)


async def generate_job_description(
    job_title: str,
    custom_note: str,
    key_focus: str,
    benefits: str | None,
) -> JobDescriptionResponse:
    """Generate a job description using Gemini with structured schema validation."""
    prompt = JOB_DESCRIPTION_PROMPT.format(
        job_title=job_title,
        custom_note=custom_note,
        key_focus=key_focus,
        benefits=benefits,
    )

    response = await generate_structured_output(
        prompt=prompt, response_model=JobDescriptionResult
    )

    if isinstance(response, LLMErrorResponse):
        raise InvalidJobRequirementsError(detail=response.error)

    return response
