from pathlib import Path
from typing import IO, Any

import requests
import streamlit as st
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError

from frontend.components.header import render_header
from frontend.components.scorecard import render_scorecard_html
from frontend.services.resume_service import analyze_resume


def load_css() -> None:
    """Load custom CSS styles."""
    css_path = Path(__file__).parents[1] / "static" / "css" / "styles.css"
    if css_path.exists():
        with css_path.open() as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.error("CSS file not found.")


def render_custom_textarea_label() -> None:
    """Apply custom style to textarea label."""
    st.markdown(
        """
        <style>
        .stTextArea label {
            color: #111827 !important;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def extract_resume_text(pdf_file: IO[bytes]) -> str:
    """Extract text from uploaded PDF file."""
    try:
        pdf = PdfReader(pdf_file)
        return "\n".join(page.extract_text() or "" for page in pdf.pages)
    except PdfReadError as e:
        st.error(f"PDF read error: {e!s}")
    except Exception as e:  # fallback for unexpected errors  # noqa: BLE001
        st.error(f"Unexpected error extracting text: {e!s}")
    return ""


def render_individual_scores(data: dict[str, Any], score_max: dict[str, int]) -> None:
    """Render the individual scorecards using components.html inside columns."""
    st.markdown("### Individual Scores")

    cols = st.columns(3)

    for idx, (label, total) in enumerate(score_max.items()):
        score = data.get(label, 0)
        with cols[idx % 3]:
            render_scorecard_html(label.replace("_", " ").title(), score, total)


def render_candidate_info(data: dict[str, Any]) -> None:
    """Display the candidate's full name if available."""
    name = data.get("candidate_name")
    if name:
        st.markdown(f"<h2>Candidate: {name}</h2>", unsafe_allow_html=True)


def render_feedback_sections(data: dict[str, Any]) -> None:
    """Render feedback sections: summary, detailed feedback, missing qualifications, suggestions."""
    st.markdown("<h3>Summary Feedback</h3>", unsafe_allow_html=True)
    st.info(data.get("summary_feedback", "No summary provided."))

    st.markdown("<h3>Detailed Feedback</h3>", unsafe_allow_html=True)
    for field, feedback in data.get("detailed_feedback", {}).items():
        label = field.replace("_feedback", "").replace("_", " ").title()
        st.write(f"**{label}:** {feedback}")

    st.markdown("<h3>Missing Qualifications</h3>", unsafe_allow_html=True)
    missing = data.get("missing_qualifications", [])
    if not missing:
        st.write("None identified.")
    for item in missing:
        st.write(f"- {item}")

    st.markdown("<h3>Improvement Suggestions</h3>", unsafe_allow_html=True)
    suggestions = data.get("improvement_suggestions", [])
    if not suggestions:
        st.write("No suggestions provided.")
    for item in suggestions:
        st.write(f"- {item}")


def render_verdict_section(data: dict[str, Any]) -> None:
    """Render the final verdict section if available."""
    verdict = data.get("verdict")
    if verdict:
        st.markdown("### Verdict")
        st.success(verdict)


# Set page config
st.set_page_config(page_title="Athena Resume Analyzer", layout="wide")

# Load CSS & custom label styling
load_css()
render_custom_textarea_label()

# Render Header
render_header()

# Upload Form
with st.form("upload_form"):
    st.subheader("Upload Resume & Paste Job Description")
    resume_file = st.file_uploader("Upload Resume (PDF Only)", type=["pdf"])
    job_description = st.text_area("Paste Job Description Here", height=200)
    submit = st.form_submit_button("Analyze Resume")

if submit:
    if not resume_file or not job_description:
        st.warning("Please upload both resume and job description.")
        st.stop()

    resume_text = extract_resume_text(resume_file)
    if not resume_text.strip():
        st.error("Resume text is empty. Please upload a valid PDF.")
        st.stop()

    try:
        data = analyze_resume(resume_text, job_description)
    except requests.exceptions.RequestException as e:
        st.error(f"Network error during resume analysis: {e!s}")
        st.stop()
    except ValueError as e:
        st.error(f"Data processing error: {e!s}")
        st.stop()
    except Exception as e:  # noqa: BLE001
        st.error(f"Unexpected error during analysis: {e!s}")
        st.stop()

    score_max = {
        "skills_match": 30,
        "experience_relevance": 20,
        "keyword_match": 15,
        "projects": 15,
        "education": 10,
        "formatting": 5,
        "additional_value": 5,
    }
    ats_score = sum(data.get(label, 0) for label in score_max)

    st.markdown(
        f"<h2>Resume Evaluation Score: {ats_score}/100</h2>", unsafe_allow_html=True
    )

    render_candidate_info(data)
    render_individual_scores(data, score_max)
    render_feedback_sections(data)
    render_verdict_section(data)

# Footer
st.markdown(
    "<div class='footer'>© 2025 Athena Resume Analyzer | Powered by 7T.ai</div>",
    unsafe_allow_html=True,
)
