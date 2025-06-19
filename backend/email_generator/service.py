from backend.core.llm import generate_text  # Import from your standardized llm.pypip
from backend.email_generator.prompts import EMAIL_GENERATION_PROMPT


async def generate_email(
    candidate: dict, verdict: str, rejection_reason: str, notes: str
) -> str:
    """Generate an email based on candidate information, verdict, rejection reason, and notes.

    Args:
        candidate (dict): Candidate information including name, title, experience, and skills.
        verdict (str): The verdict for the candidate.
        rejection_reason (str): Reason for rejection, if any.
        notes (str): Additional notes.

    Returns:
        str: The generated email text.

    """
    prompt = EMAIL_GENERATION_PROMPT.format(
        name=candidate["name"],
        title=candidate["title"],
        experience=candidate["experience"],
        skills=", ".join(candidate["skills"]),
        verdict=verdict,
        rejection_reason=rejection_reason or "N/A",
        notes=notes or "N/A",
    )

    return await generate_text(prompt)
