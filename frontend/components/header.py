import base64
from pathlib import Path

import streamlit.components.v1 as components


def get_base64_of_bin_file(bin_file: Path) -> str:
    """Convert a binary file to base64 encoded string."""
    with bin_file.open("rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def render_header() -> None:
    """Render the Athena Resume Analyzer header."""
    base_path = Path(__file__).parents[2]

    athena_logo_path = base_path / "frontend" / "static" / "images" / "Athena_logo.png"
    athena_logo_base64 = get_base64_of_bin_file(athena_logo_path)

    seven_logo_path = base_path / "frontend" / "static" / "images" / "7t-logo.svg"
    seven_logo_base64 = get_base64_of_bin_file(seven_logo_path)

    components.html(
        f"""
        <div style="
            background: linear-gradient(135deg, rgba(23,37,84,0.8) 0%, rgba(37,99,235,0.8) 100%);
            backdrop-filter: blur(15px);
            width: 100%;
            padding: 60px 50px 50px 50px;
            box-sizing: border-box;
            border-radius: 24px;
            position: relative;
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        ">
            <div style="position: absolute; top: 40px; left: 40px;">
                <img src="data:image/svg+xml;base64,{seven_logo_base64}" alt="7T.ai Logo" width="90" height="90"/>
            </div>
            <div style="display: flex; justify-content: center; align-items: center;">
                <div style="text-align: center;">
                    <img src="data:image/png;base64,{athena_logo_base64}" alt="Athena Logo" width="140" height="140" style="margin-bottom: 20px;"/>
                    <h1 style="color: white; font-size: 50px; margin: 15px 0;">Athena Resume Analyzer</h1>
                    <p style="color: white; font-size: 20px; opacity: 0.9;">AI-powered Resume Evaluation Platform</p>
                </div>
            </div>
        </div>
        """,
        height=400,
    )
