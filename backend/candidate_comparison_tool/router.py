from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .service import get_gemini_score


class ResumeInput(BaseModel):
    resume_text: str
    job_description: str


router = APIRouter(prefix="/candidate_comparison", tags=["Candidate Comparison"])


@router.post("/evaluate")
def evaluate_resume(data: ResumeInput):
    result = get_gemini_score(data.resume_text, data.job_description)
    if result.get("error"):
        raise HTTPException(status_code=500, detail=result["error"])
    return result
