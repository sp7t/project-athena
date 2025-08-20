import base64
from pathlib import Path

import streamlit as st


def load_base64_image(image_path: Path) -> str:
    """Load an image file and return its base64-encoded string."""
    with image_path.open("rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def render_header() -> None:
    """Render the header section with Athena and 7T logos."""
    athena_logo_path = (
        Path(__file__).parents[1] / "static" / "images" / "Athena_logo.png"
    )
    seven_logo_path = Path(__file__).parents[1] / "static" / "images" / "7t-logo.svg"

    athena_logo_base64 = load_base64_image(athena_logo_path)
    seven_logo_base64 = load_base64_image(seven_logo_path)

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #e9f0fc, #d7e3fc);
            border-radius: 16px;
            padding: 40px 60px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            margin-bottom: 40px;
        ">
            <div style="text-align: center; flex: 1;">
                <img src="data:image/png;base64,{athena_logo_base64}" style="width: 100px; margin-bottom: 10px;" />
                <h1 style="margin: 5px 0; color: #111827; font-size: 34px;">Athena Resume Analyzer</h1>
                <p style="color: #6b7280; font-size: 16px;">AI-powered Resume Evaluation Platform</p>
            </div>
            <div style="flex: 0;">
                <img src="data:image/svg+xml;base64,{seven_logo_base64}" style="width: 80px;" />
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
