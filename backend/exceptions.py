from fastapi import HTTPException


class APIException(HTTPException):
    """Base exception class for all API exceptions."""

    def __init__(
        self,
        status_code: int,
        detail: str,
        debug_context: str | None = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail)
        self.debug_context = debug_context

    def __str__(self) -> str:
        """Format exception for logging with debug context if available."""
        if self.debug_context:
            return f"{self.detail} [Debug Context: {self.debug_context}]"
        return self.detail
