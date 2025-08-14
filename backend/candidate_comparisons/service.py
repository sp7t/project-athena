from __future__ import annotations

import asyncio
import logging
import os
from pathlib import Path
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

# Harden env parsing for MAX_CONCURRENCY (default 3)
try:
    _max_conc = int(os.getenv("ATHENA_COMPARE_MAX_CONCURRENCY", "3"))
except (TypeError, ValueError):
    _max_conc = 3
MAX_CONCURRENCY = max(1, _max_conc)


def _to_int_0_100(value: float) -> int:
    try:
        v = float(value)
    except (ValueError, TypeError):
        v = 0.0
    v = max(0.0, min(100.0, v))
    return int(round(v))


def _map_feedback(resp: "ResumeEvaluationResponse") -> CandidateFeedback:
    data = {
        "Skills_Match": resp.skills.feedback,
        "Experience_Relevance": resp.experience.feedback,
        "Keyword_Match": resp.keywords.feedback,
        "Projects": resp.projects.feedback,
        "Education": resp.education.feedback,
        "Formatting": resp.presentation.feedback,
        "Additional_Value": resp.extras.feedback,
        "Summary": getattr(resp, "summary", None),
    }
    # Only keep fields that actually exist on the Pydantic model
    allowed = {k: v for k, v in data.items() if k in CandidateFeedback.model_fields}
    return CandidateFeedback(**allowed)


def _map_to_candidate_result(
    resp: "ResumeEvaluationResponse",
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
    overall = float(getattr(resp, "overall_score", 0.0))
    cand_data = {
        "name": resp.name,
        "score": score,
        "overall_score": _to_int_0_100(overall),
        "verdict": str(
            getattr(getattr(resp, "verdict", ""), "value", getattr(resp, "verdict", ""))
        ),
        "feedback": _map_feedback(resp),
    }
    allowed = {k: v for k, v in cand_data.items() if k in CandidateResult.model_fields}
    return CandidateResult(**allowed), overall


async def _evaluate_with_sem(
    sem: asyncio.Semaphore, r: "UploadFile", job_description: str
) -> "ResumeEvaluationResponse":
    async with sem:
        return await evaluate_resume(r, job_description)


async def compare_candidates(
    job_description: str, resumes: list["UploadFile"]
) -> CandidateComparisonResponse:
    """Compare multiple resumes against a job description and return structured results."""
    if not resumes:
        return CandidateComparisonResponse(
            candidates=[], comparison_summary="No resumes provided."
        )

    # Build tasks with sanitized display names (strip path & extension)
    tasks: list[tuple[str, asyncio.Task]] = []
    sem = asyncio.Semaphore(MAX_CONCURRENCY)

    for i, r in enumerate(resumes):
        raw_name = r.filename or f"candidate_{i + 1}"
        name_no_ext = Path(raw_name).stem or f"candidate_{i + 1}"
        tasks.append(
            (
                name_no_ext,
                asyncio.create_task(_evaluate_with_sem(sem, r, job_description)),
            )
        )

    results: list[tuple[CandidateResult, float]] = []
    failures: list[str] = []

    gathered = await asyncio.gather(*(t for _, t in tasks), return_exceptions=True)

    for (fname, _task), res in zip(tasks, gathered):
        if isinstance(res, Exception):
            logger.error(
                "Evaluation failed for %s",
                fname,
                exc_info=(type(res), res, res.__traceback__),
            )
            failures.append(f"{fname} -> {res.__class__.__name__}")
            continue
        try:
            cand, overall = _map_to_candidate_result(res)
            results.append((cand, overall))
        except Exception:
            logger.exception("Mapping failed for %s", fname)
            failures.append(f"{fname} -> MappingError")

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
        candidates=candidates_sorted,
        comparison_summary=summary,
    )
