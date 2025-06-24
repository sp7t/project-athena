import re


def extract_json_string(text: str) -> str:
    """Extract JSON object from the LLM response, removing markdown code fences if present."""
    code_fence_pattern = r"```(?:json)?\s*(\{.*?\})\s*```"
    match = re.search(code_fence_pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()
