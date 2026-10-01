"""Top-level API router."""

from typing import Literal

from fastapi import APIRouter, status
from pydantic import BaseModel

api_router = APIRouter()


class HealthResponse(BaseModel):
    """Response returned by the application health check."""

    status: Literal["ok"]


@api_router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    tags=["health"],
)
async def health_check() -> HealthResponse:
    """Report whether the API process is available."""
    return HealthResponse(status="ok")
