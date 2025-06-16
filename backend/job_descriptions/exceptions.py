from fastapi import status

from backend.exceptions import APIException


class InvalidJobRequirementsError(APIException):
    """Exception for invalid job requirements."""

    def __init__(self, detail: str) -> None:
        """Initialize InvalidJobRequirementsError."""
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid job requirements: {detail}",
        )
