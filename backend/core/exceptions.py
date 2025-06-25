from fastapi import HTTPException


class StructuredOutputError(Exception):
    """Raised when Gemini response cannot be parsed into the requested schema."""

    def __init__(
        self, schema_name: str, raw_response: str, validation_errors: str | None = None
    ) -> None:
        self.schema_name = schema_name
        self.raw_response = raw_response
        self.validation_errors = validation_errors

        base_msg = f"Failed to parse Gemini response into {schema_name}"
        if validation_errors:
            base_msg += f" [Validation Errors: {validation_errors}]"
        base_msg += f" [Raw Response: {raw_response[:500]}...]"

        super().__init__(base_msg)


class FileSizeExceededError(HTTPException):
    """Raised when file size exceeds the maximum allowed limit."""

    def __init__(
        self,
        file_size: int,
        max_size: int,
        status_code: int = 413,
        detail: str | None = None,
    ) -> None:
        self.file_size = file_size
        self.max_size = max_size

        if detail is None:
            detail = f"File size {file_size} bytes exceeds maximum allowed size of {max_size} bytes"

        super().__init__(status_code=status_code, detail=detail)


class TotalRequestSizeExceededError(HTTPException):
    """Raised when total request size exceeds the maximum allowed limit."""

    def __init__(
        self,
        total_size: int,
        max_size: int,
        status_code: int = 413,
        detail: str | None = None,
    ) -> None:
        self.total_size = total_size
        self.max_size = max_size

        if detail is None:
            detail = f"Total request size {total_size} bytes exceeds maximum allowed size of {max_size} bytes"

<<<<<<< HEAD
=======
        Args:
            detail (str): Description of the error.
            status_code (int, optional): HTTP status code. Defaults to 500.

        """
>>>>>>> c8bec4b (modified)
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
