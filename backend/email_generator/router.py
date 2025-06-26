from fastapi import APIRouter, HTTPException

from backend.core.exceptions import LLMQuotaExceeded
from backend.email_generator.schemas import EmailGenerationResponse, EmailRequest
from backend.email_generator.service import generate_email

router = APIRouter(
    prefix="/email-generator",
    tags=["Email Generator"],
)


@router.post(
    "/generate",
    status_code=200,
)
async def generate_email_endpoint(request: EmailRequest) -> EmailGenerationResponse:
    """Generate an email response based on the given candidate and verdict."""
    try:
        email_text = await generate_email(request)
        return EmailGenerationResponse(generated_email=email_text)

    except LLMQuotaExceeded as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    except Exception as exc:
        raise HTTPException(status_code=500, detail="Email generation failed") from exc
