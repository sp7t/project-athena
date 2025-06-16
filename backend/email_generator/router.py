from fastapi import APIRouter

from backend.email_generator.schemas import EmailRequest

from .service import generate_email

router = APIRouter()


@router.post("/generate")
async def generate_email_endpoint(payload: EmailRequest):  # noqa: ANN201, D103
    candidate_dict = payload.candidate.dict()
    email_text = await generate_email(
        candidate_dict,
        payload.verdict,
        payload.rejection_reason,
        payload.notes,
    )
    return {"generated_email": email_text}
