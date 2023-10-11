from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    openai_api_key: str = Field()
    aws_access_key_id: str = Field()
    aws_secret_access_key: str = Field()


def init_settings():
    settings = Settings()  # type: ignore
    print(settings)
