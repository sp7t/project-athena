from backend.exceptions import APIException


class InvalidJobRequirementsError(APIException):
    """Raised when the input to the job description service is irrelevant or inappropriate."""

    def __init__(
        self,
        status_code: int = 400,
        detail: str = "The job title or provided information does not appear valid for generating a job description.",
        debug_context: str | None = None,
    ) -> None:
        super().__init__(
            status_code=status_code, detail=detail, debug_context=debug_context
        )
