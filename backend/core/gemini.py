from typing import TypeVar

from google import genai
from pydantic import BaseModel

from backend.config import settings
from backend.core.exceptions import StructuredOutputError

# Initialize Gemini client
client = genai.Client(api_key=settings.gemini_api_key)
T = TypeVar("T", bound=BaseModel)


async def generate_text(prompt: str) -> str:
    """Generate plain text using the specified Gemini model."""
    response = await client.aio.models.generate_content(
        model=settings.gemini_model,
        contents=[prompt],
    )
    return response.text


async def generate_structured_output[T](prompt: str, response_model: type[T]) -> T:
    """Generate structured output using Gemini and validate with a Pydantic schema.

    Args:
        prompt (str): Prompt to send to Gemini.
        response_model (type[T]): Pydantic model to validate the Gemini response.

    Returns:
        T: Parsed and validated response object.

    Raises:
        StructuredOutputError: If the response cannot be parsed to the schema.

    """
    response = await client.aio.models.generate_content(
        model=settings.gemini_model,
        contents=[prompt],
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
    return response.parsed
