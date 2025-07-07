from backend.candidate_comparison_tool.schemas import (
    CandidateComparisonResponse,  # <-- fix
    CandidateResult,
)
from backend.resume_evaluations.schemas import ResumeEvaluationRequest
from backend.resume_evaluations.service import evaluate_resume


async def compare_candidates(
    job_description: str, resumes: list[str]
) -> CandidateComparisonResponse:
    """Compare multiple resumes by reusing the resume evaluation service."""
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
                "score": score.model_dump(),
            }
        )

    comparison_summary = (
        f"Compared {len(candidates)} candidates. Add custom logic for ranking."
    )

    return CandidateComparisonResponse(
        candidates=[CandidateResult(**c) for c in candidates],
        comparison_summary=comparison_summary,
    )
