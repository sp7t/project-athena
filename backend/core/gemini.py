from google import genai

from backend.config import settings

client = genai.Client(api_key=settings.gemini_api_key)


async def generate_text(prompt: str) -> str:
    """Generate text using the specified Gemini model."""
    response = await client.aio.models.generate_content(
        model=settings.gemini_model,
        contents=[prompt],
    )
    return response.text
