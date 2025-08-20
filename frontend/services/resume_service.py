# frontend/services/resume_service.py
from __future__ import annotations

import json
import os
from typing import IO, Any
from urllib.parse import urljoin

import requests

API_BASE = os.getenv("ATHENA_API_BASE", "http://127.0.0.1:8000").rstrip("/")
API_ANALYZE_PATH = os.getenv("ATHENA_ANALYZE_PATH", "/api/resume_evaluations/evaluate")
HTTP_SUCCESS_MAX = 299


class InvalidResumeFileError(TypeError):
    """Custom exception raised when the resume file does not support.

    The required methods `.getvalue()` or `.read()`.
    """

    def __init__(self) -> None:
        super().__init__("resume_file must support .getvalue() or .read().")


def _to_bytes(upload: IO[bytes]) -> bytes:
    if hasattr(upload, "getvalue"):
        return upload.getvalue()
    if hasattr(upload, "read"):
        return upload.read()
    raise InvalidResumeFileError


# Removed redundant definition of analyze_resume
def analyze_resume(resume_file: IO[bytes], job_description: str) -> dict[str, Any]:
    """Analyze a resume file against a job description.

    Parameters
    ----------
    resume_file : IO[bytes]
        The resume file to be analyzed, must support .getvalue() or .read().
    job_description : str
        The job description text to compare the resume against.

    Returns
    -------
    dict[str, Any]
        The analysis results returned by the backend.

    Raises
    ------
    InvalidResumeFileError
        If the resume file does not support .getvalue() or .read().
    requests.ConnectionError
        If there is a connection error while communicating with the backend.
    requests.HTTPError
        If the backend returns an error response or non-JSON response.

    """
    content = _to_bytes(resume_file)
    filename = getattr(resume_file, "name", "resume.pdf")
    mime = getattr(resume_file, "type", "application/pdf") or "application/pdf"

    url = (
        f"{API_BASE}{API_ANALYZE_PATH}"
        if API_ANALYZE_PATH.startswith("/")
        else urljoin(API_BASE + "/", API_ANALYZE_PATH)
    )
    files = {"resume_file": (filename, content, mime)}
    data = {"job_description": job_description}

    try:
        resp = requests.post(url, files=files, data=data, timeout=90)
    except requests.ConnectionError as err:
        msg = f"Cannot connect to backend at {url}."
        raise requests.ConnectionError(msg) from err

    if resp.status_code > HTTP_SUCCESS_MAX:
        msg = f"Backend {resp.status_code} at {url}: {resp.text[:500]}"
        raise requests.HTTPError(msg)

    try:
        return resp.json()
    except json.JSONDecodeError as err:
        msg = f"Backend returned non-JSON at {url}: {resp.text[:500]}"
        raise requests.HTTPError(msg) from err
