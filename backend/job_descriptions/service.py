from backend.core.gemini import generate_structured_output
from backend.job_descriptions.constants import JOB_DESCRIPTION_PROMPT
from backend.job_descriptions.exceptions import InvalidJobRequirementsError
from backend.job_descriptions.schemas import (
    JobDescriptionLLMOutput,
)


async def generate_job_description(
    job_title: str,
    custom_note: str,
    key_focus: str,
    benefits: str | None,
) -> str:
    """Generate a job description using Gemini with structured schema validation."""
    prompt = JOB_DESCRIPTION_PROMPT.format(
        job_title=job_title,
        custom_note=custom_note,
        key_focus=key_focus,
        benefits=benefits,
    )

    response_text = await generate_structured_output(
        prompt=prompt,
        response_model=JobDescriptionLLMOutput,
    )

    # If Gemini returned an error message instead of a description
    if response_text.error:
        raise InvalidJobRequirementsError(detail=response_text.error)

    # Fallback error in case job_description is unexpectedly missing
    if not response_text.job_description:
        raise InvalidJobRequirementsError(
            detail="Job description could not be generated."
        )

    # Return clean response model for the router
    return response_text.job_description
