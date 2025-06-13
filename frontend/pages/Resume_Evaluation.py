from pathlib import Path

import streamlit as st
from PyPDF2 import PdfReader

from frontend.components.header import render_header
from frontend.services.resume_service import analyze_resume

# — Page config & header
st.set_page_config(page_title="🦉 Athena Resume Analyzer", layout="centered")
render_header()

# css
css_path = Path(__file__).parents[1] / "static" / "css" / "styles.css"
if css_path.exists():
    with css_path.open() as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.error(f"Could not find CSS at {css_path}")

# — Upload form
with st.form("upload_form"):
    st.subheader("Upload Resume & Paste Job Description")
    resume_file = st.file_uploader("Upload Resume (PDF Only)", type=["pdf"])
    job_description = st.text_area("Paste Job Description Here", height=180)
    submit = st.form_submit_button("🚀 Analyze Resume")

# — Processing & display
if submit:
    if not resume_file or not job_description:
        st.warning("⚠️ Please upload both resume and job description.")
        st.stop()

    # extract text from PDF
    pdf = PdfReader(resume_file)
    resume_text = "\n".join(page.extract_text() or "" for page in pdf.pages)

    # call our backend/API service (no try/except needed anymore)
    data = analyze_resume(resume_text, job_description)

    # compute total ATS score
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
        f"<h2 style='color:#0052cc;'>ATS Match Score: {ats_score}/100</h2>",
        unsafe_allow_html=True,
    )

    # Individual breakdown
    st.markdown("### Individual Scores")
    cols = st.columns(3)
    for idx, (label, total) in enumerate(score_max.items()):
        score = data.get(label, 0)
        with cols[idx % 3]:
            st.metric(label.replace("_", " ").title(), f"{score}/{total}")
            st.progress(min(score / total, 1.0))

    # Summary feedback
    st.markdown("### Summary Feedback")
    st.info(data.get("summary_feedback", "No summary provided."))

    # Detailed feedback
    st.markdown("### Detailed Feedback")
    for field, feedback in data.get("detailed_feedback", {}).items():
        label = field.replace("_feedback", "").replace("_", " ").title()
        st.write(f"**{label}:** {feedback}")

    # Missing qualifications
    st.markdown("### Missing Qualifications")
    missing = data.get("missing_qualifications", [])
    if missing:
        for item in missing:
            st.write(f"- {item}")
    else:
        st.write("None identified.")

    # Improvement suggestions
    st.markdown("### Improvement Suggestions")
    suggestions = data.get("improvement_suggestions", [])
    if suggestions:
        for item in suggestions:
            st.write(f"- {item}")
    else:
        st.write("No suggestions.")
