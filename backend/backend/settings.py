from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    openai_api_key: str = Field()

    model_config = SettingsConfigDict(env_file=".env")


def init_settings():
    return Settings()  # type: ignore
