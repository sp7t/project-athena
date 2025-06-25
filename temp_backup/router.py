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
    tags=["Email Generator"],
)
async def generate_email_endpoint(request: EmailRequest) -> EmailGenerationResponse:
    """Generate an email response based on the given candidate and verdict."""
    candidate_dict = request.candidate.dict()
    try:
        email_text = await generate_email(
            candidate_dict,
            request.verdict,
            request.rejection_reason,
            request.notes,
        )
    except LLMQuotaExceeded as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Email generation failed") from exc

    return EmailGenerationResponse(generated_email=email_text)
