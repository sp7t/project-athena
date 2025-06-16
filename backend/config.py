from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings, loaded from environment variables and .env file."""

    # Gemini API key for LLM calls
    gemini_api_key: str

    # Which Gemini model to use (override in .env if needed)
    gemini_model: str = "models/gemini-1.5-flash"

    # (Optional) Supabase config for future modules
    supabase_url: str | None = None
    supabase_key: str | None = None

    model_config = SettingsConfigDict(
        # points at the reporoot .env file
        env_file=Path(__file__).resolve().parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="ignore",  # ignore any extra .env vars
    )


# single settings instance for import elsewhere
settings = Settings()
