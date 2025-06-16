from fastapi import HTTPException


class ResumeEvaluationError(HTTPException):
    """Custom exception for resume evaluation errors."""

    def __init__(self, detail: str, status_code: int = 500) -> None:
        """Initialize the resume evaluation error."""
        super().__init__(status_code=status_code, detail=detail)
