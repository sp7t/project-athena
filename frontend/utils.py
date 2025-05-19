import pyperclip

from frontend import STATIC_PATH


def load_css() -> str:
    """Load CSS from a file."""
    css_path = STATIC_PATH / "css" / "styles.css"
    with css_path.open() as f:
        return f.read()


def copy_to_clipboard(text: str) -> None:
    """Copy text to the clipboard."""
    pyperclip.copy(text)
