"""Utility functions for the backend core module."""

from pydantic import BaseModel, ValidationError


def revalidate_instance(instance: BaseModel) -> None:
    """Revalidate a Pydantic model instance.

    Args:
        instance: The Pydantic model instance to validate

    Raises:
        ValidationError: If validation fails
    """
    try:
        instance.model_validate(instance.model_dump())
    except ValidationError as e:
        raise ValidationError.from_exception_data(
            title="Validation Error", line_errors=e.errors(), model=instance.__class__
        )
