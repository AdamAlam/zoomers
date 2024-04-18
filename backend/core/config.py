import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "Letterboxd"
    PROJECT_VERSION: str = "1.0.0"

    DATABASE_URL = os.getenv("SUPABASE_URL")
    TMDB_BEARER = os.getenv("TMDB_BEARER")
    JWT_SECRET = os.getenv("JWT_SECRET")
    OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")


settings = Settings()
