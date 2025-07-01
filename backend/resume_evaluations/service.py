from backend.core.gemini import generate_structured_output
from backend.resume_evaluations.constants import RESUME_EVAL_PROMPT
from backend.resume_evaluations.schemas import (
    ResumeEvaluationRequest,
    ResumeEvaluationResponse,
)


async def evaluate_resume(request: ResumeEvaluationRequest) -> ResumeEvaluationResponse:
    """Evaluate resume using Gemini structured output and return scaled scores with total."""
    prompt = RESUME_EVAL_PROMPT.format(
        resume_text=request.resume_text,
        job_description=request.job_description,
    )

    # Call Gemini and parse
    result = await generate_structured_output(prompt, ResumeEvaluationResponse)

    # Safely ensure all raw scores exist
    skills_raw = result.skills_match or 0
    experience_raw = result.experience_relevance or 0
    keyword_raw = result.keyword_match or 0
    projects_raw = result.projects or 0
    education_raw = result.education or 0
    formatting_raw = result.formatting or 0
    additional_raw = result.additional_value or 0

    # Scale each score by its weight
    skills_match = round(skills_raw / 100 * 30, 2)
    experience_relevance = round(experience_raw / 100 * 20, 2)
    keyword_match = round(keyword_raw / 100 * 15, 2)
    projects = round(projects_raw / 100 * 15, 2)
    education = round(education_raw / 100 * 10, 2)
    formatting = round(formatting_raw / 100 * 5, 2)
    additional_value = round(additional_raw / 100 * 5, 2)

    # Final total
    total_score = round(
        skills_match
        + experience_relevance
        + keyword_match
        + projects
        + education
        + formatting
        + additional_value,
        2,
    )

    return ResumeEvaluationResponse(
        candidate_name=result.candidate_name,
        estimated_experience_years=result.estimated_experience_years,
        verdict=result.verdict,
        skills_match=skills_match,
        experience_relevance=experience_relevance,
        keyword_match=keyword_match,
        projects=projects,
        education=education,
        formatting=formatting,
        additional_value=additional_value,
        summary_feedback=result.summary_feedback,
        detailed_feedback=result.detailed_feedback,
        missing_qualifications=result.missing_qualifications,
        improvement_suggestions=result.improvement_suggestions,
        total_score=total_score,
    )
