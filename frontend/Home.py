import streamlit as st

from frontend import STATIC_PATH

st.set_page_config(page_title="Project Athena", page_icon="🦉")

logo_path = STATIC_PATH / "images" / "7t-logo.svg"

st.logo(str(logo_path))

st.title("Home")

st.write(
    "Welcome to Project Athena!",
    "This is a web application that allows you to generate job descriptions and match resumes to job descriptions.",
)
