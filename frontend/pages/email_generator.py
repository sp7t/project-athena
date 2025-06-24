import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv

# Load .env correctly from file
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

BACKEND_URL = os.getenv("EMAIL_GENERATOR_BACKEND_URL")
SENDER_EMAIL = os.getenv("EMAIL_ADDRESS")
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD")

if not all([BACKEND_URL, SENDER_EMAIL, SENDER_PASSWORD]):
    st.error("❌ Missing environment variables in .env file!")
    st.stop()

# Streamlit page config
st.set_page_config(page_title="Athena Candidate Review", layout="centered")

# Header
st.markdown(
    """
<div style="background-color: #6492CD; padding: 20px; text-align: center; border-radius: 5px;">
    <h1 style="color:white; font-size: 36px;">Athena.7t Email Generator</h1>
</div>
""",
    unsafe_allow_html=True,
)

# Logo (optional)  # noqa: ERA001
logo_path = Path(__file__).parent.parent / "logo.png"
if logo_path.exists():
    st.image(str(logo_path), width=130)

# Full Candidate Data
candidates = [
    {
        "name": "Yash",
        "email": "guijula2001@gmail.com",
        "skills": ["Python", "Machine Learning", "Data Analysis"],
        "experience": "3 years at Amazon",
        "title": "Data Scientist",
    },
    {
        "name": "Neha",
        "email": "neha.k@7t.co",
        "skills": ["UI/UX Design", "Figma", "Adobe XD"],
        "experience": "2 years at Capgemini",
        "title": "UI/UX Designer",
    },
    {
        "name": "Venkat",
        "email": "venkat.k@7t.co",
        "skills": ["Java", "Spring Boot", "AWS"],
        "experience": "4 years at Infosys",
        "title": "Backend Developer",
    },
    {
        "name": "Shashank",
        "email": "shashank.t@7t.co",
        "skills": ["React", "Node.js", "MongoDB"],
        "experience": "3.5 years at Cognizant",
        "title": "Full Stack Developer",
    },
    {
        "name": "Alvita",
        "email": "alvita@7t.co",
        "skills": ["Business Analysis", "Agile", "Stakeholder Management"],
        "experience": "5 years at Deloitte",
        "title": "Business Analyst",
    },
]

# Candidate Selection
st.title("Candidate Review")
candidate_names = [c["name"] for c in candidates]
selected_name = st.selectbox("Select Candidate", candidate_names)

# Reset session when candidate changes
if (
    "last_candidate" not in st.session_state
    or st.session_state.last_candidate != selected_name
):
    st.session_state.last_candidate = selected_name
    st.session_state.email_body = ""
    st.session_state.verdict = "Yes"
    st.session_state.rejection_reason = None
    st.session_state.notes = ""

# Load selected candidate
candidate = next(c for c in candidates if c["name"] == selected_name)

# Show candidate info
st.markdown(
    f"""
    <div style="background-color:#F5F5F5; padding:20px; border-radius:10px;">
        <b>Name:</b> {candidate["name"]}<br>
        <b>Title:</b> {candidate["title"]}<br>
        <b>Experience:</b> {candidate["experience"]}<br>
        <b>Email:</b> {candidate["email"]}<br>
        <b>Skills:</b> {", ".join(candidate["skills"])}
    </div>
    """,
    unsafe_allow_html=True,
)

# Verdict
st.session_state.verdict = st.radio("Verdict:", ["Yes", "No"])

# Rejection reason if No
if st.session_state.verdict == "No":
    st.session_state.rejection_reason = st.selectbox(
        "Rejection Reason",
        [
            "Need more experience",
            "Skills do not match",
            "Communication not clear",
            "Position already filled",
            "Not a culture fit",
        ],
    )
else:
    st.session_state.rejection_reason = None

# Optional Notes
st.session_state.notes = st.text_area("Optional Notes", value=st.session_state.notes)

# Generate email button
if st.button("Generate Email"):
    request_payload = {
        "candidate": candidate,
        "verdict": st.session_state.verdict,
        "rejection_reason": st.session_state.rejection_reason,
        "notes": st.session_state.notes,
    }

    try:
        response = requests.post(f"{BACKEND_URL}/generate", json=request_payload)  # noqa: S113
        response.raise_for_status()
        st.session_state.email_body = response.json()["generated_email"]
    except Exception as e:  # noqa: BLE001
        st.error(f"❌ Failed to generate email: {e}")

# Editable email box
if st.session_state.email_body:
    st.subheader("Generated Email")
    st.session_state.email_body = st.text_area(
        "Edit Email:", value=st.session_state.email_body, height=300
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("Send Email"):
            try:
                msg = EmailMessage()
                msg["Subject"] = "Application Status - Athena.7t"
                msg["From"] = SENDER_EMAIL
                msg["To"] = candidate["email"]
                msg.set_content(st.session_state.email_body)
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                    smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
                    smtp.send_message(msg)
                st.success("✅ Email sent successfully!")
            except Exception as e:  # noqa: BLE001
                st.error(f"❌ Failed to send email: {e}")

    with col2:
        if st.button("Save Email"):
            st.toast("Saved ✅")
