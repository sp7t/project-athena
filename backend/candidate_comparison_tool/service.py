import logging
import os
from json import JSONDecodeError, JSONDecoder

import google.generativeai as genai

from backend.candidate_comparison_tool.exceptions import (
    GeminiAPIKeyMissingError,
    JSONBlockNotFoundError,
)
from backend.candidate_comparison_tool.exceptions import (
    GeminiError as BaseGeminiError,
)
from backend.candidate_comparison_tool.prompts import build_comparison_prompt

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(level=getattr(logging, log_level.upper()))
logger = logging.getLogger(__name__)

# Check API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise GeminiAPIKeyMissingError

genai.configure(api_key=api_key)


def extract_json(text: str) -> dict:
    """Robust JSON extractor."""
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


def get_gemini_score(job_description: str, resumes: list[str]) -> dict:
    """Compare multiple resumes with a JD and return a structured summary."""
    try:
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
        prompt = build_comparison_prompt(job_description, resumes)
        response = model.generate_content(prompt)
        logger.debug("Raw Gemini response: %s", response.text)
        return extract_json(response.text)
    except Exception as e:
        msg = "Gemini comparison failed"
        raise BaseGeminiError(msg, original_exc=e) from e
