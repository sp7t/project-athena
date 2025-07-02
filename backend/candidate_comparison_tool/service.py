from backend.resume_evaluations.schemas import ResumeEvaluationRequest
from backend.resume_evaluations.service import evaluate_resume


async def compare_candidates(job_description: str, resumes: list[str]) -> dict:
    """Compare multiple resumes by reusing the resume evaluation module."""
    candidates = []

    for i, resume_text in enumerate(resumes, start=1):
        request = ResumeEvaluationRequest(
            resume_text=resume_text,
            job_description=job_description,
        )
        score = await evaluate_resume(request)
        candidates.append(
            {
                "name": f"Candidate {i}",
                "score": score.model_dump(),  # keep full structured data
            }
        )

    comparison_summary = (
        f"Compared {len(candidates)} candidates — add ranking logic here later."
    )

    return {
        "candidates": candidates,
        "comparison_summary": comparison_summary,
    }
