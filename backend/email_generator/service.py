from backend.core.gemini import generate_text
from backend.email_generator.prompts import EMAIL_GENERATION_PROMPT
from backend.email_generator.schemas import (
    EmailGenerationRequest,
    EmailGenerationResponse,
)


async def generate_email(request: EmailGenerationRequest) -> EmailGenerationResponse:
    """Generate an candidate pass/rejection email."""
    prompt = EMAIL_GENERATION_PROMPT.format(
        name=request.candidate.name,
        title=request.candidate.job_title,
        experience=request.candidate.experience,
        skills=", ".join(request.candidate.skills),
        verdict=request.verdict,
        rejection_reason=getattr(request, "reason", None),
        notes=request.notes,
    )
    generated_email = await generate_text(prompt)
    return EmailGenerationResponse(generated_email=generated_email)
