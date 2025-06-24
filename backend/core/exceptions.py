class StructuredOutputError(Exception):
    """Raised when Gemini response cannot be parsed into the requested schema."""

    def __init__(self, schema_name: str, raw_response: str) -> None:
        self.schema_name = schema_name
        self.raw_response = raw_response
        super().__init__(
            f"Failed to parse Gemini response into {schema_name} [Raw Response: {raw_response[:500]}...]"
        )
