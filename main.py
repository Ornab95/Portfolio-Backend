"""
FastAPI backend for portfolio contact form.
Receives contact form submissions and sends emails via Gmail SMTP.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

from models import ContactRequest, ContactResponse
from email_service import email_service
from config import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Validate configuration on startup
try:
    config.validate()
    logger.info("Configuration validated successfully")
except ValueError as e:
    logger.error(f"Configuration error: {e}")
    raise

# Create FastAPI app
app = FastAPI(
    title="Portfolio Contact API",
    description="API for handling contact form submissions from portfolio website",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "name": "Portfolio Contact API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "contact": "/api/contact (POST)"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "contact-api"
    }


@app.post("/api/contact", response_model=ContactResponse)
async def send_contact_email(contact: ContactRequest):
    """
    Receive contact form submission and send email.
    
    Args:
        contact: Validated contact form data
        
    Returns:
        ContactResponse with success status and message
        
    Raises:
        HTTPException: If email sending fails
    """
    try:
        logger.info(f"Received contact form submission from {contact.email}")
        
        # Prepare contact data
        contact_data = {
            "name": contact.name,
            "email": contact.email,
            "subject": contact.subject or "No Subject",
            "message": contact.message
        }
        
        # Send email
        email_service.send_email(contact_data)
        
        return ContactResponse(
            success=True,
            message="Your message has been sent successfully! We'll get back to you soon."
        )
        
    except Exception as e:
        logger.error(f"Error processing contact form: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send your message. Please try again later. Error: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
