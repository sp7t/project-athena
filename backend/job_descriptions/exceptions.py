import logging
from typing import Never

from fastapi import HTTPException

logger = logging.getLogger(__name__)


class JobDescriptionServiceError(HTTPException):
    """Custom exception for internal server errors during job description generation.

    Automatically returns a 500 Internal Server Error response.
    """

    def __init__(
        self,
        detail: str = "An internal error occurred in the job description service.",
        status_code: int = 500,
    ) -> None:
        """Initialize the service error with a custom message and status code."""
        super().__init__(status_code=status_code, detail=detail)


class InvalidJobInputError(HTTPException):
    """Raised when the input provided to the job description service is invalid or irrelevant.

    Automatically returns a 400 Bad Request response.
    """

    def __init__(
        self,
        detail: str = "The job title or provided information does not appear valid for generating a job description.",
        status_code: int = 400,
    ) -> None:
        """Initialize the invalid input error with a custom message and status code."""
        super().__init__(status_code=status_code, detail=detail)


def raise_service_error(
    message: str, original_exception: Exception | None = None
) -> Never:
    """Log and raise a JobDescriptionServiceError with optional exception chaining.

    Parameters
    ----------
    message : str
        Human-readable error message to return to the client.
    original_exception : Exception, optional
        The original exception that triggered this error (preserved in logs).

    Raises
    ------
    JobDescriptionServiceError
        Always raised to signal a 500-level internal service failure.

    """
    logger.exception(message)
    if original_exception:
        raise JobDescriptionServiceError(detail=message) from original_exception
    raise JobDescriptionServiceError(detail=message)
