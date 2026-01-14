from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    # ===== LLM Provider =====
    llm_provider: Literal["openai", "deepseek"] = "deepseek"

    llm_api_key: str
    llm_base_url: str = "https://api.deepseek.com"
    llm_model: str = "deepseek-chat"

    # ===== Embedding（Phase 5 用）=====
    embedding_provider: Literal["openai", "deepseek"] = "openai"
    embedding_model: str = "text-embedding-3-large"

    class Config:
        env_file = ".env"

settings = Settings()
