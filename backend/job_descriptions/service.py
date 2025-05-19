from backend.core.llm import generate_text
from backend.job_descriptions.prompts import JOB_DESCRIPTION_PROMPT


async def generate_job_description(title: str, details: str | None) -> str:
    """Generate a job description using an LLM."""
    prompt = JOB_DESCRIPTION_PROMPT.format(title=title, details=details)
    return await generate_text(prompt)
