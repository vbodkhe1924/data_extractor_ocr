# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    HUGGINGFACE_MODEL: str = "impira/layoutlm-invoices"
    OCR_MODEL: str = "microsoft/trocr-base-printed"
    DATABASE_URL: str = "sqlite:///invoices.db"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB

settings = Settings()