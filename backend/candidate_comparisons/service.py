from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING

from backend.candidate_comparisons.schemas import (
    CandidateComparisonResponse,
    CandidateFeedback,
    CandidateResult,
    CandidateScore,
)
from backend.resume_evaluations.service import evaluate_resume

if TYPE_CHECKING:
    from fastapi import UploadFile
    from backend.resume_evaluations.schemas import ResumeEvaluationResponse

logger = logging.getLogger(__name__)


def _to_int_0_100(value: float) -> int:
    try:
        v = float(value)
    except (ValueError, TypeError):
        v = 0.0
    v = max(0.0, min(100.0, v))
    return round(v)


def _map_feedback(resp: ResumeEvaluationResponse) -> CandidateFeedback:
    return CandidateFeedback(
        Skills_Match=resp.skills.feedback,
        Experience_Relevance=resp.experience.feedback,
        Keyword_Match=resp.keywords.feedback,
        Projects=resp.projects.feedback,
        Education=resp.education.feedback,
        Formatting=resp.presentation.feedback,
        Additional_Value=resp.extras.feedback,
        Summary=resp.summary,
    )


def _map_to_candidate_result(
    resp: ResumeEvaluationResponse,
) -> tuple[CandidateResult, float]:
    score = CandidateScore(
        Skills_Match=_to_int_0_100(resp.skills.score),
        Experience_Relevance=_to_int_0_100(resp.experience.score),
        Keyword_Match=_to_int_0_100(resp.keywords.score),
        Projects=_to_int_0_100(resp.projects.score),
        Education=_to_int_0_100(resp.education.score),
        Formatting=_to_int_0_100(resp.presentation.score),
        Additional_Value=_to_int_0_100(resp.extras.score),
    )
    overall = float(resp.overall_score)
    cand = CandidateResult(
        name=resp.name,
        score=score,
        overall_score=_to_int_0_100(overall),
        verdict=str(
            resp.verdict.value if hasattr(resp.verdict, "value") else resp.verdict
        ),
        feedback=_map_feedback(resp),
    )
    return cand, overall


async def compare_candidates(
    job_description: str, resumes: list[UploadFile]
) -> CandidateComparisonResponse:
    """Compare multiple resumes against a job description and return structured results."""
    if not resumes:
        return CandidateComparisonResponse(
            candidates=[], comparison_summary="No resumes provided."
        )

    tasks = [
        (
            r.filename or f"candidate_{i + 1}",
            asyncio.create_task(evaluate_resume(r, job_description)),
        )
        for i, r in enumerate(resumes)
    ]

    results: list[tuple[CandidateResult, float]] = []
    failures: list[str] = []

    gathered = await asyncio.gather(*(t for _, t in tasks), return_exceptions=True)

    for (fname, _), res in zip(tasks, gathered, strict=False):
        if isinstance(res, Exception):
            logger.exception("Evaluation failed for %s", fname, exc_info=res)
            failures.append(f"{fname} -> {res.__class__.__name__}: {res}")
            continue
        try:
            cand, overall = _map_to_candidate_result(res)
            results.append((cand, overall))
        except Exception as e:
            logger.exception("Mapping failed for %s", fname)
            failures.append(f"{fname} -> MappingError: {e}")

    if results:
        results.sort(key=lambda t: t[1], reverse=True)
        candidates_sorted = [c for c, _ in results]
        top3 = ", ".join(
            f"{i + 1}) {c.name} ({int(s)})" for i, (c, s) in enumerate(results[:3])
        )
        summary = f"Compared {len(candidates_sorted)} candidate(s). Top: {top3}."
    else:
        candidates_sorted = []
        summary = "No candidates could be evaluated."

    if failures:
        summary += f" Failures: {', '.join(failures)}"

    return CandidateComparisonResponse(
        candidates=candidates_sorted, comparison_summary=summary
    )
