class GeminiError(Exception):
    """Raised for all Gemini-related failures (prompt build, API call, JSON parse)."""

    def __init__(self, message: str, *, original_exc: Exception | None = None) -> None:
        """Initialize GeminiError with a message and optional original exception."""
        super().__init__(message)
        self.original_exc = original_exc

    def __str__(self) -> str:
        """Return a string representation of the GeminiError, including the original exception if present."""
        if self.original_exc:
            return f"{super().__str__()} (Caused by: {self.original_exc!r})"
        return super().__str__()


class GeminiAPIKeyMissingError(OSError):
    """Exception raised when the GEMINI API KEY environment variable is not set."""

    def __init__(self) -> None:
        """Initialize GeminiAPIKeyMissingError with a default error message."""
        super().__init__("GEMINI_API_KEY environment variable is not set")


class JSONParseError(ValueError):
    """Exception raised when JSON parsing fails."""

    def __init__(self, original_exc: Exception) -> None:
        """Initialize JSONParseError with the original exception that caused the JSON parsing to fail.

        Args:
            original_exc (Exception): The exception raised during JSON parsing.

        """
        super().__init__(f"Failed to parse JSON: {original_exc}")
        self.original_exc = original_exc

    def __str__(self) -> str:
        """Return a string representation of the JSONParseError, including the original exception."""
        return f"{super().__str__()} (Caused by: {self.original_exc!r})"


class JSONBlockNotFoundError(ValueError):
    """Exception raised when no JSON block is found in the text."""

    def __init__(self) -> None:
        """Initialize JSONBlockNotFoundError with a default error message."""
        super().__init__("JSON block not found in Gemini response")
