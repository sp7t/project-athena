import logging
import os
from json import JSONDecodeError, JSONDecoder

import google.generativeai as genai

from .exceptions import (
    GeminiAPIKeyMissingError,
    JSONBlockNotFoundError,
)
from .exceptions import (
    GeminiError as BaseGeminiError,
)
from .prompts import build_prompt

# Configure logging based on environment variable
log_level = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(level=getattr(logging, log_level.upper()))
logger = logging.getLogger(__name__)

# Check for API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise GeminiAPIKeyMissingError

# Configure Gemini
genai.configure(api_key=api_key)


def extract_json(text: str) -> dict:
    """Find and parse the first valid JSON object in the given text.

    This is more robust than regex parsing.
    """
    decoder = JSONDecoder()
    idx = 0
    while idx < len(text):
        try:
            obj, _ = decoder.raw_decode(text[idx:])
        except JSONDecodeError:
            idx += 1
        else:
            return obj
    raise JSONBlockNotFoundError


def get_gemini_score(resume_text: str, job_description: str) -> dict:
    """Send resume and JD to Gemini and return structured score breakdown as JSON.

    Raise GeminiError on failure.
    """
    try:
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
        prompt = build_prompt(resume_text, job_description)
        response = model.generate_content(prompt)
        logger.debug("Raw Gemini response: %s", response.text)
        return extract_json(response.text)
    except Exception as e:
        raise BaseGeminiError("Gemini scoring failed", original_exc=e) from e
