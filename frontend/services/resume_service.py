# frontend/services/resume_service.py
from __future__ import annotations

import json
import os
from typing import IO, Any
from urllib.parse import urljoin

import requests

API_BASE = os.getenv("ATHENA_API_BASE", "http://127.0.0.1:8000").rstrip("/")
# Set this to your real route if it differs (e.g., "/api/resume_evaluations/evaluate")
API_ANALYZE_PATH = os.getenv("ATHENA_ANALYZE_PATH", "/api/resume_evaluations/analyze")

HTTP_OK = 200
HTTP_SUCCESS_MAX = 299


class InvalidResumeFileError(TypeError):
    """Custom exception for invalid resume file."""

    def __init__(self) -> None:
        """Initialize the InvalidResumeFileError with a default error message."""
        super().__init__("resume_file must support .getvalue() or .read().")


def _to_bytes(upload: IO[bytes]) -> bytes:
    """Return file bytes from a Streamlit UploadedFile or any file-like object."""
    if hasattr(upload, "getvalue"):
        return upload.getvalue()  # type: ignore[no-any-return]
    if hasattr(upload, "read"):
        return upload.read()  # type: ignore[no-any-return]
    raise InvalidResumeFileError


def analyze_resume(resume_file: IO[bytes], job_description: str) -> dict[str, Any]:
    """Send the uploaded PDF and job description to the backend as multipart/form-data."""
    content = _to_bytes(resume_file)
    filename = getattr(resume_file, "name", "resume.pdf")
    mime = getattr(resume_file, "type", "application/pdf") or "application/pdf"

    url = (
        f"{API_BASE}{API_ANALYZE_PATH}"
        if API_ANALYZE_PATH.startswith("/")
        else urljoin(API_BASE + "/", API_ANALYZE_PATH)
    )

    files = {"file": (filename, content, mime)}
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
