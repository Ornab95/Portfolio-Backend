"""
Email service module for sending contact form emails via Gmail SMTP.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class EmailService:
    """Service for sending emails via SMTP."""
    
    def __init__(self):
        """Initialize email service with configuration."""
        self.smtp_host = settings.smtp_host
        self.smtp_port = settings.smtp_port
        self.sender_email = str(settings.sender_email)
        self.sender_password = settings.sender_password
        self.recipient_email = str(settings.recipient_email)
    
    def create_email_html(self, contact_data: Dict[str, str]) -> str:
        """
        Create HTML formatted email content.
        
        Args:
            contact_data: Dictionary containing name, email, subject, message
            
        Returns:
            HTML formatted email string
        """
        subject = contact_data.get("subject", "No Subject")
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f4f4f4;
                }}
                .content {{
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 10px 10px 0 0;
                    margin: -30px -30px 20px -30px;
                }}
                .field {{
                    margin-bottom: 15px;
                }}
                .label {{
                    font-weight: bold;
                    color: #667eea;
                }}
                .message-box {{
                    background-color: #f9f9f9;
                    padding: 15px;
                    border-left: 4px solid #667eea;
                    margin-top: 10px;
                    border-radius: 5px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="content">
                    <div class="header">
                        <h2 style="margin: 0;">New Contact Form Submission</h2>
                    </div>
                    
                    <div class="field">
                        <span class="label">From:</span> {contact_data['name']}
                    </div>
                    
                    <div class="field">
                        <span class="label">Email:</span> 
                        <a href="mailto:{contact_data['email']}">{contact_data['email']}</a>
                    </div>
                    
                    <div class="field">
                        <span class="label">Subject:</span> {subject}
                    </div>
                    
                    <div class="field">
                        <span class="label">Message:</span>
                        <div class="message-box">
                            {contact_data['message'].replace(chr(10), '<br>')}
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        return html
    
    def send_email(self, contact_data: Dict[str, str]) -> bool:
        """
        Send email with contact form data.
        
        Args:
            contact_data: Dictionary containing name, email, subject, message
            
        Returns:
            True if email was sent successfully
            
        Raises:
            Exception: If email sending fails
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            
            # Set From to show sender's name and email (via your contact form)
            sender_name = contact_data['name']
            sender_email = contact_data['email']
            msg['From'] = f"{sender_name} (via Contact Form) <{self.sender_email}>"
            
            msg['To'] = self.recipient_email
            
            # Set Reply-To to sender's actual email so you can reply directly
            msg['Reply-To'] = f"{sender_name} <{sender_email}>"
            
            # Include sender info in subject line
            subject = contact_data.get('subject', 'New Message')
            if subject and subject.lower() not in ['none', '']:
                msg['Subject'] = f"Portfolio Contact: {subject} (from {sender_name})"
            else:
                msg['Subject'] = f"Portfolio Contact: New Message (from {sender_name})"
            
            # Create HTML content
            html_content = self.create_email_html(contact_data)
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Connect to SMTP server and send email
            logger.info(f"Connecting to SMTP server: {self.smtp_host}:{self.smtp_port}")
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()  # Secure the connection
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {self.recipient_email}")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP Authentication failed: {e}")
            raise Exception("Email authentication failed. Please check credentials.")
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error occurred: {e}")
            raise Exception(f"Failed to send email: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error sending email: {e}")
            raise Exception(f"An unexpected error occurred: {str(e)}")


# Create email service instance
email_service = EmailService()
