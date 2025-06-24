from typing import Literal

from pydantic import BaseModel, model_validator


class LLMResponse(BaseModel):
    """Base response model for LLM structured output generation with success/error handling."""

    status: Literal["success", "error"]
    result: str | None = None
    error: str | None = None

    @model_validator(mode="after")
    def validate_status_fields(self) -> "LLMResponse":
        """Ensure status field matches the populated data fields."""
        if self.status == "success" and not self.result:
            msg = "Result field is required when status is 'success'"
            raise ValueError(msg)
        if self.status == "error" and not self.error:
            msg = "Error field is required when status is 'error'"
            raise ValueError(msg)
        if self.status == "success" and self.error:
            msg = "Error field must be 'None' when status is 'success'"
            raise ValueError(msg)
        if self.status == "error" and self.result:
            msg = "Result field must be 'None' when status is 'error'"
            raise ValueError(msg)
        return self
