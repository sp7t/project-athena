from backend.candidate_comparison_tool.schemas import (
    CandidateComparisonResponse,
    CandidateResult,
)
from backend.resume_evaluations.schemas import ResumeEvaluationRequest
from backend.resume_evaluations.service import evaluate_resume


async def compare_candidates(
    job_description: str, resumes: list[str]
) -> CandidateComparisonResponse:
    """Compare multiple resumes by reusing the resume evaluation service."""
    candidates = []
    failed_evaluations = []

    for i, resume_text in enumerate(resumes, start=1):
        try:
            request = ResumeEvaluationRequest(
                resume_text=resume_text,
                job_description=job_description,
            )
            score = await evaluate_resume(request)

            candidates.append(
                CandidateResult(
                    name=f"Candidate {i}",
                    score=score.model_dump(),
                )
            )
        except ValueError as e:
            failed_evaluations.append(f"Candidate {i}: {e!s}")

    candidates.sort(key=lambda c: c.score.get("score", 0), reverse=True)
    comparison_summary = f"Successfully compared {len(candidates)} candidates."
    if failed_evaluations:
        comparison_summary += f" ({len(failed_evaluations)} failed)"

    return CandidateComparisonResponse(
        candidates=candidates,
        comparison_summary=comparison_summary,
    )
