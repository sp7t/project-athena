from backend.core.gemini import generate_structured_output
from backend.email_generator.prompts import EMAIL_GENERATION_PROMPT
from backend.email_generator.schemas import (
    EmailGenerationRequest,
    EmailGenerationResponse,
)


async def generate_email(request: EmailGenerationRequest) -> EmailGenerationResponse:
    """Generate an candidate pass/rejection email."""
    prompt = EMAIL_GENERATION_PROMPT.format(
        name=request.candidate.name,
        title=request.candidate.title,
        experience=request.candidate.experience,
        skills=", ".join(request.candidate.skills),
        verdict=request.verdict,
        reason=request.reason,
        notes=request.notes,
    )
    return await generate_structured_output(prompt, EmailGenerationResponse)
