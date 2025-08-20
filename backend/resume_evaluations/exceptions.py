from backend.exceptions import APIException


class InvalidResumeFormatError(APIException):
    """Raised when the uploaded file is not a valid PDF."""

    def __init__(
        self,
        status_code: int = 415,
        detail: str = "Uploaded file is not a valid PDF. Please upload a valid PDF file.",
        debug_context: str | None = None,
    ) -> None:
        super().__init__(
            status_code=status_code, detail=detail, debug_context=debug_context
        )
