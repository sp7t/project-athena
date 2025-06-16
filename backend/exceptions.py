from fastapi import HTTPException


class APIException(HTTPException):
    """Base exception class for all API exceptions."""
