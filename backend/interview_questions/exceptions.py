from fastapi import HTTPException


class InterviewQuestionServiceError(HTTPException):
    """Exception raised for errors during interview question generation."""

    def __init__(
        self,
        detail: str = "An internal error occurred in the interview question service.",
        status_code: int = 500,
    ) -> None:
        """Initialize the InterviewQuestionServiceError.

        Args:
            detail (str): A human-readable message describing the error.
            status_code (int): HTTP status code to return with the exception. Defaults to 500.

        """
        super().__init__(status_code=status_code, detail=detail)
