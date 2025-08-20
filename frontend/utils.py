import pyperclip
from loguru import logger

from frontend import STATIC_PATH


def load_css() -> str:
    """Load CSS from a file."""
    css_path = STATIC_PATH / "css" / "styles.css"
    with css_path.open() as f:
        return f.read()


def copy_to_clipboard(text: str) -> None:
    """Copy text to the clipboard."""
    try:
        pyperclip.copy(text)
    except (OSError, RuntimeError) as e:
        logger.error(f"Failed to copy text to clipboard: {e}")
