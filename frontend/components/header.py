# Res_ev header
import streamlit.components.v1 as components


def render_header() -> None:
    """Render the black-background page header with the owl icon."""
    components.html(
        """
        <div style="background-color: #000000; padding: 40px; text-align: center; border-bottom: 2px solid #ececec;">
            <div style="display: flex; justify-content: center; align-items: center; gap: 20px;">
                <div style="font-size: 50px;">🦉</div>
                <div>
                    <h1 style="color: white; font-size: 36px; margin: 0; font-family: 'Segoe UI', sans-serif;">Athena Resume Analyzer</h1>
                    <p style="color: white; font-size: 18px; margin: 5px 0 0 0; font-family: 'Segoe UI', sans-serif;">AI-powered Resume Evaluation System</p>
                </div>
            </div>
        </div>
        """,
        height=160,
    )
