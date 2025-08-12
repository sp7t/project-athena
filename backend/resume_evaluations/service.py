from fastapi import UploadFile

from backend.core.gemini import generate_structured_output
from backend.core.schemas import FileInput, MimeType
from backend.resume_evaluations.constants import RESUME_EVAL_PROMPT
from backend.resume_evaluations.schemas import (
    BaseResumeEvaluation,
    EvaluationVerdict,
    ResumeEvaluationResponse,
)

# Category weights for total score calculation
CATEGORY_WEIGHTS = {
    "skills": 0.30,
    "experience": 0.20,
    "keywords": 0.15,
    "projects": 0.15,
    "education": 0.10,
    "presentation": 0.05,
    "extras": 0.05,
}

# Verdict score thresholds
STRONG_MATCH_THRESHOLD = 90
GOOD_MATCH_THRESHOLD = 80
PARTIAL_MATCH_THRESHOLD = 65
WEAK_MATCH_THRESHOLD = 50


def derive_verdict(score: float) -> EvaluationVerdict:
    """Map score to EvaluationVerdict enum."""
    if score >= STRONG_MATCH_THRESHOLD:
        return EvaluationVerdict.STRONG_MATCH
    if score >= GOOD_MATCH_THRESHOLD:
        return EvaluationVerdict.GOOD_MATCH
    if score >= PARTIAL_MATCH_THRESHOLD:
        return EvaluationVerdict.PARTIAL_MATCH
    if score >= WEAK_MATCH_THRESHOLD:
        return EvaluationVerdict.WEAK_MATCH
    return EvaluationVerdict.NOT_RECOMMENDED


def calculate_weighted_score(response: BaseResumeEvaluation) -> float:
    """Calculate weighted total score from category scores."""
    total = (
        response.skills.score * CATEGORY_WEIGHTS["skills"]
        + response.experience.score * CATEGORY_WEIGHTS["experience"]
        + response.keywords.score * CATEGORY_WEIGHTS["keywords"]
        + response.projects.score * CATEGORY_WEIGHTS["projects"]
        + response.education.score * CATEGORY_WEIGHTS["education"]
        + response.presentation.score * CATEGORY_WEIGHTS["presentation"]
        + response.extras.score * CATEGORY_WEIGHTS["extras"]
    )
    return round(total, 2)


def create_full_response(
    gemini_response: BaseResumeEvaluation, overall_score: float
) -> ResumeEvaluationResponse:
    """Create full response by adding calculated total score and verdict to Gemini response."""
    data = gemini_response.model_dump()
    data["overall_score"] = overall_score
    data["verdict"] = derive_verdict(overall_score)
    return ResumeEvaluationResponse.model_validate(data)


async def evaluate_resume(
    resume_file: UploadFile, job_description: str
) -> ResumeEvaluationResponse:
    """Evaluate resume using Gemini structured output and return response with calculated total score."""
    resume_content = await resume_file.read()
    resume_file_input = FileInput(data=resume_content, mime_type=MimeType.PDF)
    prompt = RESUME_EVAL_PROMPT.format(
        job_description=job_description,
    )
    gemini_response = await generate_structured_output(
        prompt=prompt, response_model=BaseResumeEvaluation, files=[resume_file_input]
    )

    total_score = calculate_weighted_score(gemini_response)
    return create_full_response(gemini_response, total_score)
