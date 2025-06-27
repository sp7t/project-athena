from pydantic import BaseModel


class LLMErrorResponse(BaseModel):
    """Generic error response from LLM structured output generation."""

    error: str
