import contextlib

from fastapi import APIRouter

from backend.email_generator.schemas import EmailGenerationResponse, EmailRequest
from backend.email_generator.service import generate_email

router = APIRouter(
    prefix="/email-generator",
    tags=["Email Generator"],
)


@router.post(
    "/generate",
    status_code=200,
    tags=["Email Generator"],
)
async def generate_email_endpoint(request: EmailRequest) -> EmailGenerationResponse:
    """Generate an email response based on the given candidate and verdict."""
    with contextlib.suppress(Exception):
        email_text = await generate_email(request)
        return EmailGenerationResponse(generated_email=email_text)
