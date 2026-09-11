import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "InsightBI AI"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    API_V1_STR: str = "/api/v1"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000"
    ]

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/insightbi"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "insightbi"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"

    # JWT Security
    SECRET_KEY: str = "c8f921a94e82b704e6b12a83c760e941a5b8214e6d7a9b01c3e4f5a6b7c8d9e0"
    JWT_SECRET: str = "c8f921a94e82b704e6b12a83c760e941a5b8214e6d7a9b01c3e4f5a6b7c8d9e0"
    ALGORITHM: str = "HS256"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # LLM / AI Copilot
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4o-mini"

    # Frontend
    NEXT_PUBLIC_API_URL: str = "http://localhost:8000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
