from dotenv import load_dotenv
from pathlib import Path
import os

# Project root directory (FastApiA-Z/)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Explicitly load .env from project root
load_dotenv(dotenv_path=BASE_DIR / ".env")

class Settings:
    GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
    SECRET_KEY: str | None = os.getenv("SECRET_KEY")
    ALGORITHM: str | None = os.getenv("ALGORITHM")

settings = Settings()
