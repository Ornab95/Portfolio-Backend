"""
FastAPI application factory.
Creates and configures the FastAPI application instance.
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.api.v1.router import api_router
from app.api.v1.endpoints.health import router as health_router

# Setup logging
setup_logging()
logger = get_logger(__name__)


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI application instance
    """
    # Only validate configuration in production, not during testing
    is_testing = os.getenv("TESTING", "false").lower() == "true"
    
    if not is_testing:
        try:
            settings.validate_required()
            logger.info("Configuration validated successfully")
        except ValueError as e:
            logger.warning(f"Configuration validation failed: {e}")
            logger.warning("Running with incomplete configuration - some features may not work")
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.app_name,
        description="API for handling contact form submissions from portfolio website",
        version=settings.app_version,
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include health check routes (at root level)
    app.include_router(health_router)
    
    # Include API v1 routes
    app.include_router(
        api_router,
        prefix="/api/v1"
    )
    
    @app.on_event("startup")
    async def startup_event():
        """Log application startup."""
        logger.info(f"{settings.app_name} v{settings.app_version} started successfully")
    
    @app.on_event("shutdown")
    async def shutdown_event():
        """Log application shutdown."""
        logger.info(f"{settings.app_name} shutting down")
    
    return app


# Create application instance
app = create_application()
