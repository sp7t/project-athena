import os

import requests
import streamlit as st
from dotenv import find_dotenv, load_dotenv
from requests import codes
from utils import copy_to_clipboard, load_css

# Load environment variables
load_dotenv(find_dotenv())
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Page configuration
st.set_page_config(page_title="Job Description Generator", page_icon="🦉")

# Load custom CSS
load_css()
st.title("Job Description Generator")

# Initialize session state variables
if "copied" not in st.session_state:
    st.session_state.copied = False
if "description" not in st.session_state:
    st.session_state.description = ""
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False


# --- API Call Function ---
def generate_job_description(
    job_title: str, custom_note: str, key_focus: str, benefits: str = ""
) -> str | None:
    """Call the backend API to generate a job description."""
    try:
        response = requests.post(
            f"{API_URL}/job-descriptions/",
            json={
                "title": job_title,
                "custom_note": custom_note,
                "key_focus": key_focus,
                "benefits": benefits,
            },
            headers={"Content-Type": "application/json"},
            timeout=30,
        )

        if response.status_code == codes.ok:
            return response.json().get("job_description", "")
        st.error(f"Error: API returned status code {response.status_code}")
    except requests.RequestException as e:
        st.error(f"Error connecting to API: {e!s}")

    return None


# --- Input Form UI ---
with st.form("job_description_form"):
    col1, col2 = st.columns(2)
    with col1:
        title_input = st.text_input(
            "Enter job title",
            placeholder="e.g., Senior Software Engineer, Product Manager, Data Scientist",
        )
        custom_note_input = st.text_input(
            "Enter custom note (e.g., US Citizens only)",
            placeholder="e.g., US Citizens only, F1 accepted, Internship...",
        )
    with col2:
        key_focus_input = st.text_area(
            "Enter key skills (comma-separated)",
            placeholder="e.g., Python, SQL, Machine Learning, Communication...",
            height=100,
        )

    st.markdown("#### Select Benefits")
    predefined_benefits = [
        "Medical Insurance",
        "Vision Insurance",
        "Dental Insurance",
        "401(k)",
        "Paid Time Off",
        "Remote Flexibility",
        "Gym Membership",
    ]
    selected_benefits = st.multiselect(
        "Select any predefined benefits:", predefined_benefits
    )
    custom_benefits = st.text_input(
        "Add custom benefits (comma-separated):",
        placeholder="e.g., Stock options, Pet insurance",
    )

    all_benefits = selected_benefits.copy()
    if custom_benefits:
        all_benefits.extend(
            [b.strip() for b in custom_benefits.split(",") if b.strip()]
        )
    benefits = "\n".join(f"- {b}" for b in all_benefits) if all_benefits else ""

    submit_button = st.form_submit_button(label="Generate Job Description")


# --- Handle Form Submission ---
if submit_button:
    if title_input and custom_note_input and key_focus_input:
        with st.spinner("Generating job description..."):
            generated = generate_job_description(
                title_input,
                custom_note_input,
                key_focus_input,
                benefits,
            )

            if generated:
                st.session_state.description = generated
                st.session_state.edit_mode = False
            else:
                st.session_state.pop("description", None)
                st.error("Failed to generate job description. Please try again later.")
    else:
        st.session_state.pop("description", None)
        st.warning("Please fill in job title, custom note, and key skills.")


# --- Display Generated Description ---
if st.session_state.get("description", ""):
    st.divider()
    st.subheader("Generated Job Description")

    col1, col2 = st.columns(2)

    # Copy Button
    with col1:
        copy_button = st.button("Copy", key="copy_btn_persistent")
        if copy_button:
            copy_to_clipboard(st.session_state.description)
        if st.session_state.get("copied", False):
            st.toast("Copied to clipboard", icon="✅")
            st.session_state.copied = False

    # Download Button
    with col2:
        st.download_button(
            label="Download",
            data=st.session_state.description,
            file_name="job_description.md",
            mime="text/markdown",
            key="download_btn_persistent",
        )

    # Display in view or edit mode
    if not st.session_state.edit_mode:
        with st.container(border=True):
            st.markdown(st.session_state.description)
        if st.button("Edit"):
            st.session_state.edit_mode = True
    else:
        st.session_state.description = st.text_area(
            "Edit the job description below:",
            value=st.session_state.description,
            height=400,
        )
        if st.button("Save"):
            st.session_state.edit_mode = False
