"""
Contact form endpoints.
"""
from fastapi import APIRouter, HTTPException

from app.schemas.contact import ContactRequest, ContactResponse
from app.services.email import email_service
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("/contact", response_model=ContactResponse)
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
