import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from workspace root or current directory
root_dir = Path(__file__).resolve().parent.parent.parent
dotenv_path = root_dir / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path)
else:
    load_dotenv()

class Settings:
    # Server Settings
    AI_HOST: str = os.getenv("AI_HOST", "127.0.0.1")
    AI_PORT: int = int(os.getenv("AI_PORT", "8000"))
    
    # AI API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY", "")
    
    # Amadeus Flight Credentials (Optional)
    AMADEUS_CLIENT_ID: str = os.getenv("AMADEUS_CLIENT_ID", "")
    AMADEUS_CLIENT_SECRET: str = os.getenv("AMADEUS_CLIENT_SECRET", "")
    
    # StayingAPI Hotel Credentials (Optional)
    STAYINGAPI_KEY: str = os.getenv("STAYINGAPI_KEY", "")
    
    # Database URL
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mongodb://localhost:27017/travelsync")

settings = Settings()
