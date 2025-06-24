from typing import TypeVar

from google import generativeai as genai
from pydantic import BaseModel, ValidationError

from backend.config import settings
from backend.core.constants import GEMINI_MAX_TOTAL_REQUEST_SIZE
from backend.core.exceptions import StructuredOutputError, TotalRequestSizeExceededError
from backend.core.schemas import FileInput
from backend.core.utils import validate_instance

client = genai.Client(api_key=settings.genai_api_key)

T = TypeVar("T", bound=BaseModel)


async def _validate_total_request_size(
    prompt: str,
    files: list[FileInput] | None = None,
) -> None:
    """Validate that the total request size doesn't exceed the limit."""
    total_size = len(prompt.encode("utf-8"))

    if files:
        file_sizes = []
        for f in files:
            file_bytes = await f.get_file_bytes_async()
            file_sizes.append(len(file_bytes))
        total_size += sum(file_sizes)

    if total_size > GEMINI_MAX_TOTAL_REQUEST_SIZE:
        raise TotalRequestSizeExceededError(
            total_size=total_size,
            max_size=GEMINI_MAX_TOTAL_REQUEST_SIZE,
        )


async def generate_structured_output(
    prompt: str, response_model: type[T], files: list[FileInput] | None = None
) -> T:
    """Generate structured output from Gemini and parse it using the provided Pydantic model.

    Args:
        prompt: The text prompt.
        response_model: Pydantic model class for structured output.
        files: Optional list of file inputs.

    Returns:
        T: The parsed structured output.

    """
    await _validate_total_request_size(prompt, files)

    contents = []

    if files:
        file_parts = []
        for f in files:
            file_bytes = await f.get_file_bytes_async()
            file_parts.append(
                genai.Part.from_bytes(
                    data=file_bytes,
                    mime_type=f.mime_type.value,
                )
            )
        contents.extend(file_parts)

    contents.append(prompt)

    response = await client.aio.models.generate_content(
        model=settings.genai_model,
        contents=contents,
        config={
            "response_mime_type": "application/json",
            "response_schema": response_model,
        },
    )

    if response.parsed is None:
        raise StructuredOutputError(
            schema_name=response_model.__name__,
            raw_response=response.text,
        )

    try:
        validate_instance(response.parsed)
    except ValidationError as e:
        error_details = []
        for error in e.errors():
            field = ".".join(str(loc) for loc in error["loc"])
            msg = error["msg"]
            error_details.append(f"{field}: {msg}")

        raise StructuredOutputError(
            schema_name=response_model.__name__,
            raw_response=response.text,
            validation_errors=" | ".join(error_details),
        ) from None

    return response.parsed
