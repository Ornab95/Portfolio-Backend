"""
Pytest configuration and fixtures.
"""
import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

# Set testing flag before importing app
os.environ["TESTING"] = "true"

from app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def mock_email_service():
    """Mock the email service to avoid sending real emails during tests."""
    with patch("app.services.email.email_service") as mock:
        mock.send_email = MagicMock(return_value=True)
        yield mock


@pytest.fixture
def sample_contact_data():
    """Sample contact form data for testing."""
    return {
        "name": "Test User",
        "email": "test@example.com",
        "subject": "Test Subject",
        "message": "This is a test message for unit testing purposes."
    }
