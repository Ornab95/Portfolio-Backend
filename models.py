"""
Pydantic models for request validation and response formatting.
"""
from pydantic import BaseModel, EmailStr, Field


class ContactRequest(BaseModel):
    """Model for contact form submission data."""
    
    name: str = Field(..., min_length=2, max_length=100, description="Sender's name")
    email: EmailStr = Field(..., description="Sender's email address")
    subject: str | None = Field(None, max_length=200, description="Email subject")
    message: str = Field(..., min_length=10, max_length=5000, description="Message content")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "subject": "Regarding your portfolio",
                "message": "Hello! I'm interested in discussing a potential project with you."
            }
        }


class ContactResponse(BaseModel):
    """Model for API response."""
    
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Response message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Your message has been sent successfully!"
            }
        }
