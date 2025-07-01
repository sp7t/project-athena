from backend.exceptions import APIException


class ResumeEvaluationError(APIException):
    """Base exception for resume evaluation failures."""

    def __init__(
        self,
        status_code: int = 500,
        detail: str = "An error occurred during resume evaluation.",
        debug_context: str | None = None,
    ) -> None:
        super().__init__(
            status_code=status_code, detail=detail, debug_context=debug_context
        )


class InvalidResumeFormatError(ResumeEvaluationError):
    """Raised when the uploaded file is not a valid PDF."""

    def __init__(self) -> None:
        super().__init__(
            status_code=400,
            detail="Uploaded file is not a valid PDF. Please upload a valid PDF file.",
        )


class MissingResumeFileError(ResumeEvaluationError):
    """Raised when no resume file is uploaded."""

    def __init__(self) -> None:
        super().__init__(
            status_code=400,
            detail="No resume file uploaded. Please attach a PDF resume.",
        )


class MissingJobDescriptionError(ResumeEvaluationError):
    """Raised when no job description is provided."""

    def __init__(self) -> None:
        super().__init__(
            status_code=400,
            detail="Job description is missing. Please paste the job description.",
        )
