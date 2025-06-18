class GeminiError(Exception):
    """Raised for all Gemini-related failures (prompt build, API call, JSON parse)."""

    def __init__(self, message: str, *, original_exc: Exception | None = None) -> None:
        """Initialize GeminiError with a message and optional original exception."""
        super().__init__(message)
        self.original_exc = original_exc
