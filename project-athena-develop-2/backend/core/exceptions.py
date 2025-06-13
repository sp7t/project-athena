from fastapi import HTTPException


class LLMGenerationError(HTTPException):
    """Custom exception for errors during LLM text generation."""

    def __init__(self, detail: str, status_code: int = 500) -> None:
        """Initialize LLMGenerationError."""
        super().__init__(status_code=status_code, detail=detail)
