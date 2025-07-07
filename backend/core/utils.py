from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def revalidate_instance(instance: T) -> None:
    """Re-validate a Pydantic model instance using its current field values.

    Args:
        instance: Any Pydantic model instance

    Raises:
        ValidationError: If the current field values don't pass validation

    """
    # Get the model class
    model_class = instance.__class__

    # Extract current field values
    current_data = instance.model_dump()

    # Re-validate using the model's validator
    model_class.model_validate(current_data)
