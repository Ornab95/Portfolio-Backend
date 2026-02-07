"""
Pydantic schemas for contact form validation and responses.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class ContactRequest(BaseModel):
    """Schema for contact form submission data."""
    
    name: str = Field(
        ..., 
        min_length=2, 
        max_length=100, 
        description="Sender's name",
        examples=["John Doe"]
    )
    email: EmailStr = Field(
        ..., 
        description="Sender's email address",
        examples=["john.doe@example.com"]
    )
    subject: Optional[str] = Field(
        None, 
        max_length=200, 
        description="Email subject",
        examples=["Regarding your portfolio"]
    )
    message: str = Field(
        ..., 
        min_length=10, 
        max_length=5000, 
        description="Message content",
        examples=["Hello! I'm interested in discussing a potential project with you."]
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "subject": "Regarding your portfolio",
                    "message": "Hello! I'm interested in discussing a potential project with you."
                }
            ]
        }
    }


class ContactResponse(BaseModel):
    """Schema for API response."""
    
    success: bool = Field(
        ..., 
        description="Whether the operation was successful"
    )
    message: str = Field(
        ..., 
        description="Response message"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "success": True,
                    "message": "Your message has been sent successfully!"
                }
            ]
        }
    }
