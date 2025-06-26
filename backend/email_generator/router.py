from fastapi import APIRouter

from backend.email_generator.schemas import (
    EmailGenerationRequest,
    EmailGenerationResponse,
)
from backend.email_generator.service import generate_email

# Initialize the router with prefix and tags
router = APIRouter(
    prefix="/email-generator",
    tags=["Email Generator"],
)


@router.post(
    "/generate",
    status_code=200,
    summary="Generate Candidate Email",
    description="Generate an email response based on the given candidate information and verdict.",
)
async def generate_email_endpoint(
    request: EmailGenerationRequest,
) -> EmailGenerationResponse:
    """Generate an email response based on the given candidate and verdict.

    Args:
        request (EmailRequest): The request body containing candidate info, verdict, etc.

    Returns:
        EmailGenerationResponse: The generated email text.

    """
    return await generate_email(request)
