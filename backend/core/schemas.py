from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field, field_validator

from backend.core.constants import GEMINI_MAX_FILE_SIZE
from backend.core.exceptions import FileSizeExceededError


class LLMErrorResponse(BaseModel):
    """Generic error response from LLM structured output generation."""

    error: str


class MimeType(str, Enum):
    """Accepted MIME types for Gemini document processing.

    See: https://ai.google.dev/gemini-api/docs/document-processing?lang=python#technical-details
    """

    PDF = "application/pdf"
    JAVASCRIPT_APP = "application/x-javascript"
    JAVASCRIPT_TEXT = "text/javascript"
    PYTHON_APP = "application/x-python"
    PYTHON_TEXT = "text/x-python"
    TXT = "text/plain"
    HTML = "text/html"
    CSS = "text/css"
    MARKDOWN = "text/md"
    CSV = "text/csv"
    XML = "text/xml"
    RTF = "text/rtf"


class FileInput(BaseModel):
    """Schema for file input with validation."""

    data: bytes | Path | str = Field(
        description="File data as bytes, Path object, or file path string"
    )
    mime_type: MimeType = Field(description="MIME type of the file")

    @field_validator("data")
    @classmethod
    def validate_file_size(
        cls,
        v: bytes | Path | str,
    ) -> bytes | Path | str:
        """Validate file size doesn't exceed maximum."""
        if isinstance(v, bytes):
            file_size = len(v)
        elif isinstance(v, (Path, str)):
            file_path = Path(v)
            if not file_path.exists():
                msg = f"File not found: {file_path}"
                raise ValueError(msg)
            file_size = file_path.stat().st_size
        else:
            msg = f"Unsupported file data type: {type(v)}"
            raise TypeError(msg)

        if file_size > GEMINI_MAX_FILE_SIZE:
            raise FileSizeExceededError(file_size, GEMINI_MAX_FILE_SIZE)

        return v

    def get_file_bytes(self) -> bytes:
        """Get file content as bytes."""
        if isinstance(self.data, bytes):
            return self.data
        if isinstance(self.data, (Path, str)):
            try:
                file_path = Path(self.data)
                return file_path.read_bytes()
            except FileNotFoundError as e:
                msg = f"File not found: {self.data}"
                raise FileNotFoundError(msg) from e
            except PermissionError as e:
                msg = f"Permission denied reading file: {self.data}"
                raise PermissionError(msg) from e
        msg = f"Unsupported file data type: {type(self.data)}"
        raise TypeError(msg)
