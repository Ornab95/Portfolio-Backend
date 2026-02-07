"""
Tests for contact endpoint.
"""
import pytest
from unittest.mock import patch


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "contact-api"
    }


def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert "endpoints" in data


def test_contact_endpoint_success(client, sample_contact_data):
    """Test successful contact form submission."""
    with patch("app.api.v1.endpoints.contact.email_service") as mock_service:
        mock_service.send_email.return_value = True
        
        response = client.post("/api/v1/contact", json=sample_contact_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "successfully" in data["message"].lower()
        
        # Verify email service was called
        mock_service.send_email.assert_called_once()


def test_contact_endpoint_validation_error(client):
    """Test contact form with invalid data."""
    invalid_data = {
        "name": "A",  # Too short (min 2 chars)
        "email": "invalid-email",  # Invalid email format
        "message": "Short"  # Too short (min 10 chars)
    }
    
    response = client.post("/api/v1/contact", json=invalid_data)
    assert response.status_code == 422  # Validation error


def test_contact_endpoint_missing_fields(client):
    """Test contact form with missing required fields."""
    incomplete_data = {
        "name": "Test User"
        # Missing email and message
    }
    
    response = client.post("/api/v1/contact", json=incomplete_data)
    assert response.status_code == 422  # Validation error


def test_contact_endpoint_email_service_error(client, sample_contact_data):
    """Test contact form when email service fails."""
    with patch("app.api.v1.endpoints.contact.email_service") as mock_service:
        mock_service.send_email.side_effect = Exception("SMTP connection failed")
        
        response = client.post("/api/v1/contact", json=sample_contact_data)
        
        assert response.status_code == 500
        data = response.json()
        assert "failed" in data["detail"].lower()


def test_contact_endpoint_optional_subject(client):
    """Test contact form without optional subject field."""
    data_without_subject = {
        "name": "Test User",
        "email": "test@example.com",
        "message": "This is a test message without a subject."
    }
    
    with patch("app.api.v1.endpoints.contact.email_service") as mock_service:
        mock_service.send_email.return_value = True
        
        response = client.post("/api/v1/contact", json=data_without_subject)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
