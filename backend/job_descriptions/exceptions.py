from fastapi import HTTPException


class JobDescriptionServiceError(HTTPException):
    """Custom exception for errors during job description service operations."""

    def __init__(
        self,
        detail: str = "An internal error occurred in the job description service.",
        status_code: int = 500,
    ) -> None:
        """Initialize JobDescriptionServiceError."""
        super().__init__(status_code=status_code, detail=detail)
