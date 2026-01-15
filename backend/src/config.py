"""Application configuration from environment variables."""


from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database Configuration
    database_url: str = "postgresql://postgres:postgres@localhost:5432/todo_app"

    # Better Auth Configuration
    better_auth_secret: str = "your-secret-key-min-32-characters-long"

    # Server Configuration
    debug: bool = True
    environment: str = "development"

    # CORS Configuration
    allowed_origins: list[str] = ["http://localhost:3000", "http://localhost:8000"]

    # API Configuration
    api_version: str = "v1"

    # Error Tracking Configuration (T152)
    sentry_dsn: str | None = None
    sentry_traces_sample_rate: float = 1.0
    sentry_profiles_sample_rate: float = 1.0

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
