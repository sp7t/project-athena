from backend.core.gemini import generate_structured_output
from backend.core.schemas import LLMErrorResponse
from backend.job_descriptions.constants import JOB_DESCRIPTION_PROMPT
from backend.job_descriptions.exceptions import (
    InvalidJobRequirementsError,
)
from backend.job_descriptions.schemas import (
    JobDescriptionLLMResponse,
    JobDescriptionResponse,
)


async def generate_job_description(
    job_title: str,
    custom_note: str,
    key_focus: str,
    benefits: str | None,
) -> JobDescriptionResponse:
    """
    Generates a structured job description using Gemini based on the provided job title, custom note, key focus, and optional benefits.
    
    Parameters:
        job_title (str): The title of the job position.
        custom_note (str): Additional notes or context to include in the job description.
        key_focus (str): The main focus or requirements for the job.
        benefits (str | None): Optional benefits to highlight in the job description.
    
    Returns:
        JobDescriptionResponse: A validated structured response containing the generated job description.
    
    Raises:
        InvalidJobRequirementsError: If the language model returns an error response.
    """
    prompt = JOB_DESCRIPTION_PROMPT.format(
        job_title=job_title,
        custom_note=custom_note,
        key_focus=key_focus,
        benefits=benefits,
    )

    response = await generate_structured_output(
        prompt=prompt, response_model=JobDescriptionLLMResponse
    )

    if isinstance(response, LLMErrorResponse):
        raise InvalidJobRequirementsError(detail=response.error)

    return response
