from fastapi import HTTPException


class LLMGenerationError(HTTPException):
    """Custom exception for errors during LLM text generation."""

    def __init__(self, detail: str, status_code: int = 500) -> None:
        """Initialize LLMGenerationError with a detail message and optional status code.

        Args:
            detail (str): Description of the error.
            status_code (int, optional): HTTP status code. Defaults to 500.

        """
        super().__init__(status_code=status_code, detail=detail)


class LLMQuotaExceeded(HTTPException):
    """Custom exception for quota exhaustion from LLM providers."""

    def __init__(
        self, detail: str = "LLM quota exceeded", status_code: int = 429
    ) -> None:
        """Initialize LLMQuotaExceeded with a detail message and optional status code.

        Args:
            detail (str, optional): Description of the error. Defaults to "LLM quota exceeded".
            status_code (int, optional): HTTP status code. Defaults to 429.

        """
        super().__init__(status_code=status_code, detail=detail)
