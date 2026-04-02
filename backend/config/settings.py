import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Legal Document Analyzer"
    VERSION: str = "1.0.0"

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Uploads
    UPLOAD_DIR: str = "uploads"

    # ML Models
    MODEL_PATH: str = "ml/artifacts/risk_model.pkl"
    TFIDF_PATH: str = "ml/artifacts/tfidf.pkl"
    LABEL_ENCODER_PATH: str = "ml/artifacts/label_encoder.pkl"

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./legal_docs.db")

    # API Keys
    OPENAI_API_KEY: str | None = None
    HUGGINGFACE_API_KEY: str | None = None

    class Config:
        env_file = ".env"
        extra = "allow"   # Important fix


settings = Settings()