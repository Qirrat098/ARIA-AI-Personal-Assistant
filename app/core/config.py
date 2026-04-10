from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    
    openai_api_key: str | None = Field(None, validation_alias="OPENAI_API_KEY")
    database_url: str = Field("sqlite:///./assistant.db", validation_alias="DATABASE_URL")
    openai_model: str = Field("gpt-4o-mini", validation_alias="OPENAI_MODEL")
    app_title: str = Field("AI Personal Assistant", validation_alias="APP_TITLE")
    cors_origins: list[str] = Field(["*"], validation_alias="CORS_ORIGINS")

settings = Settings()
