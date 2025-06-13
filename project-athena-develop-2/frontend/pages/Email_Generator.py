import os  # noqa: I001
import smtplib
from email.message import EmailMessage
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
# === Load .env correctly from current file path ===
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)
SENDER_EMAIL = os.getenv("EMAIL_ADDRESS")
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not all([SENDER_EMAIL, SENDER_PASSWORD, GEMINI_API_KEY]):
    st.error(
        ":x: One or more environment variables are missing. Please check your .env file."
    )
    st.stop()
# === Gemini setup ===
try:
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
except ImportError:
    st.error(":x: google-generativeai module not installed.")
    st.stop()
# === Streamlit config ===
st.set_page_config(page_title="Athena Candidate Review", layout="centered")
# === Header ===
st.markdown(
    """
    <div style="background-color: #6492CD; padding: 20px; text-align: center; border-radius: 5px;">
        <h1 style="color:white; font-size: 36px;">Athena.7t</h1>
    </div>
""",
    unsafe_allow_html=True,
)
# === Logo Loading (dynamic path safe) ===
logo_path = Path(__file__).parent / "logo.png"
st.image(str(logo_path), width=130)
# === Custom CSS ===
st.markdown(
    """
<style>
.candidate-info {
    background-color: #F5F5F5;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    margin-top: 20px;
    margin-bottom: 30px;
}
.stButton > button {
    background-color: #4B0082 !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.4rem !important;
    border: none !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    background-color: #3E0074 !important;
    transform: scale(1.02) !important;
}
</style>
""",
    unsafe_allow_html=True,
)
# === Candidate Data ===
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
# === Candidate Selection ===
st.title("Candidate Review Dashboard")
candidate_names = [c["name"] for c in candidates]
selected_name = st.selectbox(
    "Select a candidate to review:", candidate_names, key="candidate_select"
)
# === Reset state on candidate change ===
if (
    "last_candidate" not in st.session_state
    or st.session_state.last_candidate != selected_name
):
    st.session_state.last_candidate = selected_name
    st.session_state.verdict = None
    st.session_state.rejection_reason = None
    st.session_state.additional_notes = ""
    st.session_state.email_body = ""
# === Fetch Candidate Data ===
candidate = next(c for c in candidates if c["name"] == selected_name)
# === Display Candidate Info ===
st.markdown(
    f"""
<div class="candidate-info">
  <h3>Candidate Info</h3>
  <p><strong>Name:</strong> {candidate["name"]}</p>
  <p><strong>Title:</strong> {candidate["title"]}</p>
  <p><strong>Email:</strong> {candidate["email"]}</p>
  <p><strong>Experience:</strong> {candidate["experience"]}</p>
  <p><strong>Skills:</strong></p>
  <ul>{"".join(f"<li>{skill}</li>" for skill in candidate["skills"])}</ul>
</div>
""",
    unsafe_allow_html=True,
)
# === Verdict ===
st.session_state.verdict = st.radio(
    "Select your verdict:",
    ["Yes", "No"],
    horizontal=True,
    index=0
    if st.session_state.verdict is None
    else (0 if st.session_state.verdict == "Yes" else 1),
)
# === Rejection Reason ===
if st.session_state.verdict == "No":
    st.session_state.rejection_reason = st.selectbox(
        "Reason for rejection:",
        [
            "Need more experience",
            "Skills do not match",
            "Communication not clear",
            "Position already filled",
            "Not a culture fit",
        ],
        index=0
        if st.session_state.rejection_reason is None
        else [
            "Need more experience",
            "Skills do not match",
            "Communication not clear",
            "Position already filled",
            "Not a culture fit",
        ].index(st.session_state.rejection_reason),
    )
else:
    st.session_state.rejection_reason = None
# === Additional Notes ===
st.session_state.additional_notes = st.text_area(
    "Optional Notes to include in email:",
    value=st.session_state.additional_notes,
    placeholder="Write any extra info you want included...",
)
# === Gemini Email Generation Logic ===
def generate_email(candidate, verdict, rejection_reason, notes):  # noqa: ANN001, ANN201, D103
    prompt = f"""
You are an HR recruiter at Athena.7t. Generate a professional email to communicate the candidate's screening result.
Candidate Details:
- Name: {candidate["name"]}
- Role: {candidate["title"]}
- Experience: {candidate["experience"]}
- Skills: {", ".join(candidate["skills"])}
- Verdict: {verdict}
- Rejection Reason: {rejection_reason if rejection_reason else "N/A"}
- HR Notes: {notes if notes else "N/A"}
Instructions:
- If Verdict is 'Yes':
  - Inform the candidate that they've successfully cleared the initial screening.
  - Mention that the next stage will involve further assessments and interviews.
  - DO NOT mention final offer or job confirmation.
  - Use language like: "move forward", "next steps", "interview process", "further evaluation".
- If Verdict is 'No':
  - Politely decline.
  - Clearly mention reason for rejection.
  - Encourage the candidate to apply again in future.
- Tone: professional, polite, warm, clear, human-like.
- Keep total word count between 120 to 160 words.
"""
    response = model.generate_content(prompt)
    return response.text
# === Generate Email Button ===
if st.button("Generate Email"):
    st.session_state.email_body = generate_email(
        candidate,
        st.session_state.verdict,
        st.session_state.rejection_reason,
        st.session_state.additional_notes,
    )
# === Show Editor if email generated ===
if st.session_state.email_body:
    st.subheader("Generated Email (Editable)")
    st.session_state.email_body = st.text_area(
        "Edit before sending:", value=st.session_state.email_body, height=300
    )
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("Send Email"):
            subject = "Application Status - Athena.7t"
            try:
                msg = EmailMessage()
                msg["Subject"] = subject
                msg["From"] = SENDER_EMAIL
                msg["To"] = candidate["email"]
                msg.set_content(st.session_state.email_body)
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                    smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
                    smtp.send_message(msg)
                st.success(":white_check_mark: Email sent successfully!")
            except smtplib.SMTPException as e:
                st.error(f":x: Email failed: {e}")
    with col2:
        if st.button("Save Email"):
            st.toast("Saved", icon=":white_check_mark:")
