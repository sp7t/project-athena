from pathlib import Path
from typing import Any

import requests
import streamlit as st

from frontend.components.header import render_header
from frontend.services.resume_service import analyze_resume

# ---------- helpers ----------


def load_css() -> None:
    """Load custom CSS styles."""
    css_path = Path(__file__).parents[1] / "static" / "css" / "styles.css"
    if css_path.exists():
        with css_path.open() as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def render_custom_textarea_label() -> None:
    """Apply custom style to textarea label and local styles."""
    st.markdown(
        """
        <style>
        .stTextArea label { color: #111827 !important; font-weight: 600; }
        .kpi { font-size: 1.75rem; font-weight: 700; margin: 0.5rem 0 1.25rem; }
        .candidate-name { font-size: 1.5rem; font-weight: 800; margin: .25rem 0 1rem; }
        .detail-line { margin: .35rem 0 .35rem; line-height: 1.5; }
        .section-title { margin-top: 1.75rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def get_overall_score(payload: dict[str, Any]) -> int:
    """Best-effort extraction of overall score (int 0-100)."""
    for key in ("overall_score", "total_score", "ats_score", "score"):
        val = payload.get(key)
        if isinstance(val, (int, float)):
            return round(val)
    # fallback: average category scores if present
    cats = [
        payload.get("skills", {}),
        payload.get("experience", {}),
        payload.get("keywords", {}),
        payload.get("projects", {}),
        payload.get("education", {}),
        payload.get("presentation", {}),
        payload.get("extras", {}),
    ]
    scores = [
        c.get("score")
        for c in cats
        if isinstance(c, dict) and isinstance(c.get("score"), (int, float))
    ]
    return round(sum(scores) / len(scores)) if scores else 0


def render_category_lines(payload: dict[str, Any]) -> None:
    """Render 'Category (NN/100): feedback' lines, skipping missing."""
    categories: list[tuple[str, str]] = [
        ("skills", "Skills Match"),
        ("experience", "Experience Relevance"),
        ("keywords", "Keyword Match"),
        ("projects", "Projects"),
        ("education", "Education"),
        ("presentation", "Formatting"),
        ("extras", "Additional Value"),
    ]

    st.markdown("### Detailed Feedback", unsafe_allow_html=True)
    for key, label in categories:
        block = payload.get(key)
        if not isinstance(block, dict):
            continue
        score = block.get("score")
        feedback = block.get("feedback") or "—"
        score_txt = (
            f"{round(score)}/100" if isinstance(score, (int, float)) else "—/100"
        )
        st.markdown(
            f"<div class='detail-line'><strong>{label} ({score_txt}):</strong> {feedback}</div>",
            unsafe_allow_html=True,
        )


def render_optional_list(title: str, items: str | list[str]) -> None:
    """Render a list section if items exist (handles str or list[str])."""
    st.markdown(f"### {title}", unsafe_allow_html=True)
    if not items:
        st.write("None identified.")
        return
    if isinstance(items, str):
        st.write(items)
        return
    if isinstance(items, list):
        for it in items:
            st.write(f"- {it}")


# ---------- page setup ----------

st.set_page_config(page_title="Athena Resume Analyzer", layout="wide")
load_css()
render_custom_textarea_label()
render_header()

# ---------- form ----------

with st.form("upload_form"):
    st.subheader("Upload Resume & Paste Job Description")
    resume_file = st.file_uploader("Upload Resume (PDF Only)", type=["pdf"])
    job_description = st.text_area("Paste Job Description Here", height=200)
    submit = st.form_submit_button("Analyze Resume")

# ---------- submission ----------

if submit:
    if resume_file is None or not job_description.strip():
        st.warning("Please upload both resume and job description.")
        st.stop()

    try:
        with st.spinner("Analyzing your resume..."):
            data: dict[str, Any] = analyze_resume(resume_file, job_description)
    except requests.exceptions.RequestException as e:
        st.error(f"Network error during resume analysis: {e!s}")
        st.stop()
    except ValueError as e:
        st.error(f"Data processing error: {e!s}")
        st.stop()
    except Exception as e:  # noqa: BLE001
        st.error(f"Unexpected error during analysis: {e!s}")
        st.stop()

    # ---- top KPI (no weights shown) ----
    overall = get_overall_score(data)
    st.markdown(
        f"<div class='kpi'>Overall Score: {overall}/100</div>",
        unsafe_allow_html=True,
    )

    # ---- candidate name (bigger & bold) ----
    name = data.get("name") or data.get("candidate_name")
    if isinstance(name, str) and name.strip():
        st.markdown(
            f"<div class='candidate-name'>Candidate: {name}</div>",
            unsafe_allow_html=True,
        )

    # ---- summary ----
    summary = data.get("summary") or data.get("summary_feedback")
    if isinstance(summary, str) and summary.strip():
        st.markdown("### Summary", unsafe_allow_html=True)
        st.info(summary)

    # ---- detailed lines like 'Skills Match (62/100): ...' ----
    render_category_lines(data)

    # ---- optional sections (supports old + new keys) ----
    missing_items = (
        data.get("missing_qualifications") or data.get("missing_requirements") or []
    )
    render_optional_list("Missing Qualifications", missing_items)

    suggestions = (
        data.get("improvement_suggestions") or data.get("recommendations") or []
    )
    render_optional_list("Improvement Suggestions", suggestions)

    # ---- verdict ----
    verdict = data.get("verdict")
    if isinstance(verdict, str) and verdict.strip():
        st.markdown("### Verdict", unsafe_allow_html=True)
        st.success(verdict)

# ---------- footer ----------
st.markdown(
    "<div class='footer'>© 2025 Athena Resume Analyzer | Powered by 7T.ai</div>",
    unsafe_allow_html=True,
)
