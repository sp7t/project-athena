from typing import TypeVar

from google import genai
from google.genai import types
from pydantic import BaseModel, ValidationError

from backend.config import settings
from backend.core.exceptions import StructuredOutputError
from backend.core.schemas import FileInput
from backend.core.utils import revalidate_instance

client = genai.Client(api_key=settings.gemini_api_key)

T = TypeVar("T", bound=BaseModel)


async def generate_text(prompt: str, files: list[FileInput] | None = None) -> str:
    """Generate free-form text using the specified Gemini model.

    Args:
        prompt: The text prompt
        files: Optional list of file inputs

    Returns:
        str: The generated text

    """
    contents = []

    if files:
        contents.extend(
            types.Part.from_bytes(data=f.get_file_bytes(), mime_type=f.mime_type.value)
            for f in files
        )

    contents.append(prompt)

    response = await client.aio.models.generate_content(
        model=settings.gemini_model,
        contents=contents,
    )

    return response.text


async def generate_structured_output(
    prompt: str,
    response_model: type[T],
    files: list[FileInput] | None = None,
) -> T:
    """Generate structured output from Gemini and parse it using the provided Pydantic model.

    Args:
        prompt: The text prompt
        response_model: Pydantic model class for structured output
        files: Optional list of file inputs

    Returns:
        T: The parsed structured output

    """
    contents = []

    if files:
        contents.extend(
            types.Part.from_bytes(data=f.get_file_bytes(), mime_type=f.mime_type.value)
            for f in files
        )

    contents.append(prompt)

    response = await client.aio.models.generate_content(
        model=settings.gemini_model,
        contents=contents,
        config={
            "response_mime_type": "application/json",
            "response_schema": response_model,
        },
    )

    if response.parsed is None:
        raise StructuredOutputError(
            schema_name=response_model.__name__, raw_response=response.text
        )

    try:
        # Re-validate the parsed response
        revalidate_instance(response.parsed)
    except ValidationError as e:
        # Format validation errors cleanly
        error_details = []
        for error in e.errors():
            field = ".".join(str(loc) for loc in error["loc"])
            msg = error["msg"]
            error_details.append(f"{field}: {msg}")

        raise StructuredOutputError(
            schema_name=response_model.__name__,
            raw_response=response.text,
            validation_errors="; ".join(error_details),
        ) from e

    return response.parsed
