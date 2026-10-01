"""FastAPI application bootstrap."""

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    application = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        debug=settings.debug,
    )
    application.include_router(api_router, prefix=settings.api_v1_prefix)
    return application


app = create_application()
