from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field


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

    def get_file_bytes(self) -> bytes:
        """Get file content as bytes."""
        if isinstance(self.data, bytes):
            return self.data
        if isinstance(self.data, (Path, str)):
            return Path(self.data).read_bytes()
        msg = f"Unsupported file data type: {type(self.data)}"
        raise TypeError(msg)
