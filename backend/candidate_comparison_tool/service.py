import json
import os
import re

import google.generativeai as genai

from .prompts import build_prompt

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON: {e}")
    else:
        raise ValueError("JSON block not found in Gemini response")


def get_gemini_score(resume_text, job_description):
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    prompt = build_prompt(resume_text, job_description)
    try:
        response = model.generate_content(prompt)
        response_json = extract_json(response.text)
        return response_json
    except Exception as e:
        return {"error": str(e)}
