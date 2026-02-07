"""
Configuration module for FastAPI contact form backend.
Loads and validates environment variables.
"""
import os
from dotenv import load_dotenv

# Load environment variables from config.env file
load_dotenv('config.env')


class Config:
    """Application configuration loaded from environment variables."""
    
    # Email configuration
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SENDER_EMAIL: str = os.getenv("SENDER_EMAIL", "")
    SENDER_PASSWORD: str = os.getenv("SENDER_PASSWORD", "")
    RECIPIENT_EMAIL: str = os.getenv("RECIPIENT_EMAIL", "")
    
    # CORS configuration
    ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "*").split(",")
    
    @classmethod
    def validate(cls) -> None:
        """Validate that required configuration is present."""
        required_vars = {
            "SENDER_EMAIL": cls.SENDER_EMAIL,
            "SENDER_PASSWORD": cls.SENDER_PASSWORD,
            "RECIPIENT_EMAIL": cls.RECIPIENT_EMAIL,
        }
        
        missing = [key for key, value in required_vars.items() if not value]
        
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}"
            )


# Create config instance
config = Config()
