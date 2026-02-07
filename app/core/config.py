"""
Core configuration module using Pydantic Settings.
Loads and validates environment variables with better type safety.
"""
from typing import List
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

# Get the project root directory (parent of app directory)
PROJECT_ROOT = Path(__file__).parent.parent.parent
CONFIG_FILE = PROJECT_ROOT / "config.env"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=str(CONFIG_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Email configuration
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    sender_email: str = ""
    sender_password: str = ""
    recipient_email: str = ""
    
    # CORS configuration
    allowed_origins: str = "*"
    
    # Application settings
    app_name: str = "Portfolio Contact API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    @field_validator("allowed_origins")
    @classmethod
    def parse_origins(cls, v: str) -> List[str]:
        """Parse comma-separated origins into a list."""
        if v == "*":
            return ["*"]
        return [origin.strip() for origin in v.split(",")]
    
    def validate_required(self) -> None:
        """Validate that all required settings are present."""
        required_fields = {
            "sender_email": self.sender_email,
            "sender_password": self.sender_password,
            "recipient_email": self.recipient_email,
        }
        
        missing = [key for key, value in required_fields.items() if not value]
        
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}"
            )


# Create global settings instance
settings = Settings()
