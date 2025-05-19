from google import genai

from backend.config import settings
from backend.core.exceptions import LLMGenerationError

client = genai.Client(api_key=settings.gemini_api_key)


async def generate_text(prompt: str) -> str:
    """Generate text using the specified Gemini model."""
    try:
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=[prompt],
        )
    except Exception as e:
        raise LLMGenerationError(detail=str(e)) from e

    return response.text
