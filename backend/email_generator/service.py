from backend.core.gemini import generate_text
from backend.email_generator.prompts import EMAIL_GENERATION_PROMPT
from backend.email_generator.schemas import EmailRequest


async def generate_email(request: EmailRequest) -> str:
    """Generate an email based on the EmailRequest object.

    Args:
        request (EmailRequest): Includes candidate info, verdict, rejection reason, and notes.

    Returns:
        str: The generated email text.

    """
    prompt = EMAIL_GENERATION_PROMPT.format(
        name=request.candidate.name,
        title=request.candidate.title,
        experience=request.candidate.experience,
        skills=", ".join(request.candidate.skills),
        verdict=request.verdict,
        rejection_reason=request.rejection_reason or "N/A",
        notes=request.notes or "N/A",
    )

    return await generate_text(prompt)
