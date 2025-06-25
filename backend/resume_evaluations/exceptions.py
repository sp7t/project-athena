from backend.exceptions import APIException


class ResumeEvaluationError(APIException):
    """Custom exception for resume evaluation failures."""

    def __init__(
        self,
        status_code: int = 500,
        detail: str = "An error occurred during resume evaluation.",
        debug_context: str | None = None,
    ) -> None:
        super().__init__(
            status_code=status_code, detail=detail, debug_context=debug_context
        )
