import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory for the project
BASE_DIR = Path(__file__).resolve().parent

# Load .env file from the project directory (override=True ensures edits to .env take immediate effect on reload)
load_dotenv(BASE_DIR / ".env", override=True)

def _sanitize_api_key(raw_val: str) -> str:
    """Cleans API key and filters out common placeholder values so unconfigured keys are treated as empty."""
    if not raw_val:
        return ""
    cleaned = raw_val.strip().strip('"').strip("'")
    placeholders = {
        "your_gemini_api_key_here",
        "your_actual_gemini_api_key_here",
        "your_api_key_here",
        "your_api_key",
        "your_gemini_api_key",
        "api_key_here",
        "placeholder",
        "none",
        "null"
    }
    if cleaned.lower() in placeholders:
        return ""
    return cleaned

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "learnmate-hackathon-insecure-secret-key-change-in-prod")
    DATABASE_PATH = os.environ.get("DATABASE_PATH", str(BASE_DIR / "learnmate.db"))
    
    # Upload configurations
    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_CONTENT_LENGTH", 2 * 1024 * 1024))  # 2MB max
    ALLOWED_EXTENSIONS = {"txt", "md", "vtt", "srt"}
    
    # AI API Keys
    GEMINI_API_KEY = _sanitize_api_key(os.environ.get("GEMINI_API_KEY", ""))
    OPENAI_API_KEY = _sanitize_api_key(os.environ.get("OPENAI_API_KEY", ""))
    AI_PROVIDER = os.environ.get("AI_PROVIDER", "gemini").strip().lower()  # 'gemini' or 'openai' or 'demo'
    GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash").strip() or "gemini-1.5-flash"
    
    # Text limits
    MIN_CONTENT_CHARS = 120
    MAX_CONTENT_CHARS = 40000
