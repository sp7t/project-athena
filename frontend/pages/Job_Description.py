import os

import requests
import streamlit as st
from dotenv import find_dotenv, load_dotenv
from requests import codes
from utils import copy_to_clipboard, load_css

# Load environment variables
load_dotenv(find_dotenv())
API_URL = os.getenv("API_URL", "http://localhost:8000/api")

# Page configuration
st.set_page_config(page_title="Job Description Generator", page_icon="🦉")

# Load custom CSS
load_css()

st.title("Job Description Generator")

# Initialize session state for copy success message
if "copied" not in st.session_state:
    st.session_state.copied = False


# Function to call the backend API
def generate_job_description(job_title: str, job_details: str) -> str | None:
    """Call the backend API to generate a job description."""
    try:
        response = requests.post(
            f"{API_URL}/job-descriptions/",
            json={"title": job_title, "details": job_details},
            headers={"Content-Type": "application/json"},
            timeout=30,
        )

        if response.status_code == codes.ok:
            return response.json().get("job_description", "")
        st.error(f"Error: API returned status code {response.status_code}")
    except requests.RequestException as e:
        st.error(f"Error connecting to API: {e!s}")

    return None


# Create the form for job description generation
with st.form("job_description_form"):
    title_input = st.text_input(
        "Enter job title",
        placeholder="e.g., Senior Software Engineer, Product Manager, Data Scientist",
    )
    details_input = st.text_area(
        "Enter job details (optional)",
        placeholder="e.g., Key responsibilities, required skills, company culture...",
        height=150,
    )

    submit_button = st.form_submit_button(label="Generate")

# Handle form submission
if submit_button:
    if title_input:
        # Show a spinner while generating
        with st.spinner("Generating job description..."):
            # Call API to generate job description
            # Use a temporary variable for the newly generated description
            newly_generated_description = generate_job_description(
                title_input, details_input
            )

            if newly_generated_description:
                # Store the description in session state
                st.session_state.description = newly_generated_description
            else:
                # If generation fails, clear any existing description from session state
                if "description" in st.session_state:
                    del st.session_state.description
                st.error("Failed to generate job description. Please try again later.")
    else:
        # If title is missing, also clear any existing description
        if "description" in st.session_state:
            del st.session_state.description
        st.warning("Please enter a job title first.")

# Display generated job description if it exists in session state
# This block is now outside and independent of the `if submit_button:` block for display persistence
if "description" in st.session_state and st.session_state.description:
    st.divider()
    st.subheader("Generated Job Description")

    # Create action buttons
    col1, col2 = st.columns(2)

    # Copy button
    with col1:
        copy_button = st.button(
            "Copy", key="copy_btn_persistent"
        )  # Changed key to avoid conflict if old one lingers
        if copy_button:
            copy_to_clipboard(
                st.session_state.description
            )  # Use description from session state

        # Show success message if copied
        if st.session_state.get("copied", False):  # Use .get for safer access
            st.toast("Copied to clipboard", icon="✅")
            # Reset after showing
            st.session_state.copied = False

    # Download button
    with col2:
        st.download_button(
            label="Download",
            data=st.session_state.description,  # Use description from session state
            file_name="job_description.md",
            mime="text/markdown",
            key="download_btn_persistent",  # Changed key
        )

    # Display content in the styled container
    with st.container(border=True):
        st.markdown(st.session_state.description)  # Use description from session state
