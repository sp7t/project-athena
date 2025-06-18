import logging
import os
from json import JSONDecodeError, JSONDecoder

import google.generativeai as genai

from .exceptions import GeminiError as BaseGeminiError
from .prompts import build_prompt


# -------------------------------
# Exception for missing API Key
# -------------------------------
class GeminiAPIKeyMissingError(OSError):
    """Exception raised when the GEMINI API KEY environment variable is not set."""

    def __init__(self) -> None:
        """Initialize the exception for missing GEMINI_API_KEY environment variable."""
        super().__init__("GEMINI_API_KEY environment variable is not set")


# -------------------------------
# Fail fast if GEMINI_API_KEY is missing
# -------------------------------
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise GeminiAPIKeyMissingError

genai.configure(api_key=api_key)

# Enable logging for development
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# -------------------------------
# Parsing Exceptions
# -------------------------------
class JSONParseError(ValueError):
    """Exception raised when JSON parsing fails.

    Attributes
    ----------
    original_exc : Exception
        The original exception that caused the JSON parsing to fail.

    """

    def __init__(self, original_exc: Exception) -> None:
        """Initialize JSONParseError with the original exception that caused the failure."""
        super().__init__(f"Failed to parse JSON: {original_exc}")
        self.original_exc = original_exc


class JSONBlockNotFoundError(ValueError):
    """Exception raised when a JSON block is not found in the Gemini response."""

    def __init__(self) -> None:
        """Initialize JSONBlockNotFoundError indicating no JSON block was found in the response."""
        super().__init__("JSON block not found in Gemini response")


# -------------------------------
# Robust JSON Extraction
def extract_json(text: str) -> dict:
    """Find and parse the first valid JSON object in the given text.

    This is more robust than regex parsing.
    """
    decoder = JSONDecoder()
    idx = 0
    while idx < len(text):
        try:
            obj, end = decoder.raw_decode(text[idx:])
        except JSONDecodeError:
            idx += 1  # Slide forward one char and retry
        else:
            return obj
    raise JSONBlockNotFoundError
    raise JSONBlockNotFoundError


# -------------------------------
# Custom GeminiError Wrapper
# -------------------------------
class GeminiError(BaseGeminiError):
    """Exception raised when Gemini scoring fails.

    Attributes
    ----------
    original_exc : Exception
        The original exception that caused the Gemini scoring to fail.

    """

    def __init__(self, original_exc: Exception) -> None:
        """Initialize GeminiError with the original exception that caused the failure."""
        super().__init__(f"Gemini scoring failed: {original_exc}")
        self.original_exc = original_exc


# -------------------------------
# Main scoring function
# -------------------------------
def get_gemini_score(resume_text: str, job_description: str) -> dict:
    """Send resume and JD to Gemini and return structured score breakdown as JSON.

    Raise GeminiError on failure.
    """
    try:
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
        prompt = build_prompt(resume_text, job_description)
        response = model.generate_content(prompt)
        logger.debug("Raw Gemini response: %s", response.text)  # Dev-only logging
        return extract_json(response.text)
    except Exception as e:
        raise GeminiError(e) from e
