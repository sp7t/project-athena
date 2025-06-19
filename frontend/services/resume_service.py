import requests


def analyze_resume(resume_text: str, job_description: str) -> dict:
    """Call backend API to analyze resume and return evaluation dict."""
    resp = requests.post(
        "http://localhost:8000/api/resume_evaluations/evaluate",
        json={"resume_text": resume_text, "job_description": job_description},
        timeout=10,
    )

    resp.raise_for_status()
    return resp.json()
