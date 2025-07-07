from backend.exceptions import APIException


class StructuredOutputError(Exception):
    """Raised when Gemini response cannot be parsed into the requested schema."""

    def __init__(
        self, schema_name: str, raw_response: str, validation_errors: str | None = None
    ) -> None:
        self.schema_name = schema_name
        self.raw_response = raw_response
        self.validation_errors = validation_errors

        # Build the error message
        base_msg = f"Failed to parse Gemini response into {schema_name}"
        if validation_errors:
            base_msg += f" [Validation Errors: {validation_errors}]"
        base_msg += f" [Raw Response: {raw_response[:500]}...]"

        super().__init__(base_msg)


class FileSizeExceededError(APIException):
    """Raised when file size exceeds the maximum allowed limit."""

    def __init__(
        self,
        file_size: int,
        max_size: int,
        status_code: int = 413,
        detail: str | None = None,
        debug_context: str | None = None,
    ) -> None:
        self.file_size = file_size
        self.max_size = max_size

        if detail is None:
            detail = f"File size {file_size} bytes exceeds maximum allowed size of {max_size} bytes"

        super().__init__(
            status_code=status_code, detail=detail, debug_context=debug_context
        )
