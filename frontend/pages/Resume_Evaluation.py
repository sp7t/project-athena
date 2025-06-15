# --- resume_evaluation.py ---
from pathlib import Path

import streamlit as st
from PyPDF2 import PdfReader

from frontend.components.header import render_header
from frontend.services.resume_service import analyze_resume

# Page config
st.set_page_config(page_title="🦉 Athena Resume Analyzer", layout="wide")

# Apply global dark mode safety (extra guarantee)
st.markdown(
    """
    <style>
        html, body, .stApp {
            background-color: #111827 !important;
            color: #f1f5f9 !important;
        }
    </style>
""",
    unsafe_allow_html=True,
)


# Render header
render_header()

# Load CSS
css_path = Path(__file__).parents[1] / "static" / "css" / "styles.css"
if css_path.exists():
    with css_path.open() as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.error(f"CSS file not found at {css_path}")

# Upload Form
with st.form("upload_form"):
    st.subheader("Upload Resume & Paste Job Description")
    resume_file = st.file_uploader("Upload Resume (PDF Only)", type=["pdf"])
    job_description = st.text_area("Paste Job Description Here", height=180)
    submit = st.form_submit_button("Analyze Resume")

if submit:
    if not resume_file or not job_description:
        st.warning("Please upload both resume and job description.")
        st.stop()

    pdf = PdfReader(resume_file)
    resume_text = "\n".join(page.extract_text() or "" for page in pdf.pages)

    data = analyze_resume(resume_text, job_description)

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
        f"<h2 class='score-title'>Resume Evaluation Score: {ats_score}/100</h2>",
        unsafe_allow_html=True,
    )

    st.markdown("### Individual Scores")
    cols = st.columns(3)
    for idx, (label, total) in enumerate(score_max.items()):
        score = data.get(label, 0)
        with cols[idx % 3]:
            st.metric(label.replace("_", " ").title(), f"{score}/{total}")
            st.progress(min(score / total, 1.0))

    st.markdown("<div class='card'><h3>Summary Feedback</h3>", unsafe_allow_html=True)
    st.info(data.get("summary_feedback", "No summary provided."))
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><h3>Detailed Feedback</h3>", unsafe_allow_html=True)
    for field, feedback in data.get("detailed_feedback", {}).items():
        label = field.replace("_feedback", "").replace("_", " ").title()
        st.write(f"**{label}:** {feedback}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        "<div class='card'><h3>Missing Qualifications</h3>", unsafe_allow_html=True
    )
    missing = data.get("missing_qualifications", [])
    for item in missing:
        st.write(f"- {item}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        "<div class='card'><h3>Improvement Suggestions</h3>", unsafe_allow_html=True
    )
    suggestions = data.get("improvement_suggestions", [])
    for item in suggestions:
        st.write(f"- {item}")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    "<div class='footer'>© 2025 Athena Resume Analyzer | Powered by 7T.ai</div>",
    unsafe_allow_html=True,
)
