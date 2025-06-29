from typing import TypeVar

from google import genai
from pydantic import BaseModel

from backend.config import settings
from backend.core.exceptions import StructuredOutputError

client = genai.Client(api_key=settings.gemini_api_key)

T = TypeVar("T", bound=BaseModel)


async def generate_text(prompt: str) -> str:
    """Generate text using the specified Gemini model."""
    response = await client.aio.models.generate_content(
        model=settings.gemini_model,
        contents=[prompt],
    )
    return response.text or ""


async def generate_structured_output(prompt: str, response_model: type[T]) -> T:
    """Generate structured output using the specified Gemini model and Pydantic schema."""
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
            schema_name=response_model.__name__, raw_response=response.text or ""
        )

    return response_model.parse_obj(response.parsed)
