from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str = ""
    API_BASE_URL: str = ""

    REDIS_URL: str = "redis://localhost:6379/1"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
