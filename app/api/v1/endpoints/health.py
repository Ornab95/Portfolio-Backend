"""
Health check endpoints.
"""
from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "endpoints": {
            "health": "/health",
            "contact": "/api/v1/contact (POST)"
        }
    }


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "contact-api"
    }
