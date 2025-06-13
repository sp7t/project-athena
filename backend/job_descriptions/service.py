import traceback

from backend.core.llm import generate_text
from backend.job_descriptions.exceptions import (
    InvalidJobInputError,
    JobDescriptionServiceError,
)
from backend.job_descriptions.prompts import (
    JOB_BENEFITS_SECTION,
    JOB_DESCRIPTION_TEMPLATE,
    PROMPT_SUFFIX,
)
from backend.job_descriptions.validator import is_irrelevant


async def generate_job_description(
    job_title: str, custom_note: str, key_focus: str, benefits: str = ""
) -> str:
    """Generate a structured, markdown-formatted job description using an LLM."""
    # Input validation for professionalism and relevance
    if any(map(is_irrelevant, [job_title, custom_note, key_focus])):
        raise InvalidJobInputError

    try:
        # Build the main prompt
        prompt = JOB_DESCRIPTION_TEMPLATE.format(
            job_title=job_title, custom_note=custom_note, key_focus=key_focus
        )

        # Optionally add benefits section
        if benefits.strip():
            prompt += "\n\n" + JOB_BENEFITS_SECTION.format(benefits=benefits)

        # Add guardrails and final check
        prompt += "\n\n" + PROMPT_SUFFIX

        # Call Gemini LLM via wrapper
        return await generate_text(prompt)

    except Exception as e:
        traceback.print_exc()
        raise JobDescriptionServiceError(detail=str(e)) from e
