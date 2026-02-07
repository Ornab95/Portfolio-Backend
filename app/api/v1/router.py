"""
API v1 Router.
Includes all v1 endpoints.
"""
from fastapi import APIRouter

from app.api.v1.endpoints import contact

api_router = APIRouter()

# Include contact endpoints
api_router.include_router(
    contact.router,
    tags=["contact"]
)
