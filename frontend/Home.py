import base64
from pathlib import Path

import streamlit as st

from frontend import STATIC_PATH

st.set_page_config(page_title="Athena HR Toolkit", page_icon="🦉", layout="centered")

# Inject custom CSS styling (same as your original)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FFFFFF;
    }

    .container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 90vh;
    }

    .logo {
        width: 140px;
        margin-bottom: 20px;
    }

    .title {
        font-size: 36px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 50px;
    }

    .button-container {
        display: flex;
        gap: 50px;
        flex-wrap: wrap;
        justify-content: center;
    }

    .button {
    background-color: #2F7EDB;
    color: white !important;
    padding: 20px 60px;
    border-radius: 12px;
    text-decoration: none !important;
    font-size: 18px;
    font-weight: 600;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}

.button:hover {
    background-color: #2566B8;
}


    .top-right-logo {
        position: fixed;
        top: 70px;
        right: 40px;
        width: 120px;
        z-index: 999;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def get_base64(file_path: Path) -> str:
    """Return base64 string from given file path."""
    with file_path.open("rb") as f:
        return base64.b64encode(f.read()).decode()


# Load logos
athena_logo_path: Path = STATIC_PATH / "images" / "Athena_logo.png"
seven_logo_path: Path = STATIC_PATH / "images" / "7t-logo.svg"

athena_logo_base64 = get_base64(athena_logo_path)
seven_logo_base64 = get_base64(seven_logo_path)

# Display 7t.ai logo on top right
st.markdown(
    f"""
    <div class="top-right-logo">
        <img src="data:image/svg+xml;base64,{seven_logo_base64}" alt="7t.ai Logo">
    </div>
    """,
    unsafe_allow_html=True,
)

# Main UI Content
st.markdown(
    f"""
    <div class="container">
        <img class="logo" src="data:image/png;base64,{athena_logo_base64}" alt="Athena Logo"/>
        <div class="title">Athena HR Toolkit</div>
        <div class="button-container">
            <a class="button" href="/Resume_Evaluation" target="_self">Resume Evaluation</a>
            <a class="button" href="/Job_Description" target="_self">Job Description Generator</a>
            <a class="button" href="/Candidate_Comparison" target="_self">Candidate Comparison</a>
            <a class="button" href="/Email_Generator" target="_self">Email Generator</a>
            <a class="button" href="/Interview_Questions" target="_self">Interview Questions Generator</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
