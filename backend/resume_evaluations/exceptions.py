from fastapi import HTTPException


class ResumeEvaluationError(HTTPException):
    """Raised when the resume-evaluation service fails."""

    def __init__(
        self, detail: str = "Resume evaluation failed.", status_code: int = 500
    ) -> None:
        """Initialize with an HTTP status code and detail message."""
        super().__init__(status_code=status_code, detail=detail)
