import json
import os

import google.generativeai as genai
from dotenv import load_dotenv

from .exceptions import ResumeEvaluationError
from .prompts import RESUME_EVAL_PROMPT

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
_MODEL = genai.GenerativeModel("models/gemini-1.5-flash")


def evaluate_resume(resume_text: str, job_description: str) -> dict:
    """Call Gemini to evaluate the resume and parse the JSON response."""
    prompt = RESUME_EVAL_PROMPT.format(
        resume_text=resume_text,
        job_description=job_description,
    )
    try:
        resp = _MODEL.generate_content(prompt)
        raw = resp.text
        body = raw[raw.find("{") : raw.rfind("}") + 1]
        return json.loads(body)
    except json.JSONDecodeError as err:
        msg = f"JSON parse error: {err}"
        raise ResumeEvaluationError(msg) from err
