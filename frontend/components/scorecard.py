import streamlit.components.v1 as components


def render_scorecard_html(label: str, score: int, total: int) -> None:
    """Render an individual scorecard as HTML using components.html()."""
    percentage = (score / total) * 100

    card_html = f"""
    <div style="
        background-color: #1f2937;
        padding: 15px 20px;
        border-radius: 12px;
        margin: 10px 15px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        width: 250px;
        display: inline-block;
        vertical-align: top;">
        <div style="
            color: #ffffff;
            font-weight: 600;
            font-size: 16px;
            margin-bottom: 8px;
            text-align: center;">
            {label}
        </div>
        <div style="
            color: #ffffff;
            font-weight: 700;
            font-size: 32px;
            text-align: center;">
            {score}/{total}
        </div>
        <div style="
            margin-top: 12px;
            background-color: #374151;
            height: 8px;
            border-radius: 5px;
            overflow: hidden;">
            <div style="
                width: {percentage}%;
                height: 100%;
                background-color: #ff006a;">
            </div>
        </div>
    </div>
    """

    components.html(card_html, height=200, scrolling=False)
