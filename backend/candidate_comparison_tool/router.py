from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .exceptions import GeminiError
from .service import get_gemini_score

router = APIRouter()


class ResumeInput(BaseModel):
    """Input model for resume evaluation.

    Attributes
    ----------
    resume_text : str
        The text content of the candidate's resume.
    job_description : str
        The job description to compare against the resume.

    """

    resume_text: str
    job_description: str


@router.post("/evaluate", status_code=200, tags=["Candidate Comparison"])
async def evaluate_resume(data: ResumeInput) -> dict:
    """Evaluate a candidate's resume against a job description and return a score.

    Parameters
    ----------
    data : ResumeInput
        The input data containing resume text and job description.

    Returns
    -------
    dict
        The evaluation score and related information.

    Raises
    ------
    HTTPException
        If there is an error during evaluation.

    """
    try:
        return get_gemini_score(data.resume_text, data.job_description)
    except GeminiError as ge:
        raise HTTPException(status_code=503, detail=str(ge)) from ge
