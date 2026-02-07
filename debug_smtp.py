"""
Debug script to test SMTP connection and verify credentials.
"""
import smtplib
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv('config.env')

print("=== SMTP Configuration Debug ===")
print(f"SMTP Host: {os.getenv('SMTP_HOST')}")
print(f"SMTP Port: {os.getenv('SMTP_PORT')}")
print(f"Sender Email: {os.getenv('SENDER_EMAIL')}")
print(f"Password Length: {len(os.getenv('SENDER_PASSWORD', ''))}")
print(f"Password (masked): {'*' * len(os.getenv('SENDER_PASSWORD', ''))}")
print()

try:
    print("Attempting to connect to Gmail SMTP...")
    smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    
    print(f"Connecting to {smtp_host}:{smtp_port}")
    server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
    print("✓ Connected to SMTP server")
    
    print("Starting TLS...")
    server.starttls()
    print("✓ TLS started")
    
    print(f"Logging in as {sender_email}...")
    server.login(sender_email, sender_password)
    print("✓ Login successful!")
    
    server.quit()
    print("\n✅ SMTP connection test PASSED!")
    print("Your Gmail credentials are working correctly.")
    
except smtplib.SMTPAuthenticationError as e:
    print(f"\n❌ Authentication failed: {e}")
    print("\nPossible issues:")
    print("1. App password is incorrect")
    print("2. 2-Step Verification is not enabled on your Google account")
    print("3. You need to generate a new App Password at:")
    print("   https://myaccount.google.com/apppasswords")
    
except Exception as e:
    print(f"\n❌ Connection error: {e}")
    print(f"Error type: {type(e).__name__}")
