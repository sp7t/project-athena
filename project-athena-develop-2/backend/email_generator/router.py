from fastapi import APIRouter  # noqa: I001, INP001
from backend.email_generator.service import generate_email
from backend.email_generator.schemas import EmailRequest

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
