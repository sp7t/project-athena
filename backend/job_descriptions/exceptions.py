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


class InvalidJobInputError(HTTPException):
    """Raised when the input to the job description service is irrelevant or inappropriate."""

    def __init__(
        self,
        detail: str = "The job title or provided information does not appear valid for generating a job description.",
        status_code: int = 400,
    ) -> None:
        """Initialize the InvalidJobInputError with a detail message and status code."""
        super().__init__(status_code=status_code, detail=detail)
