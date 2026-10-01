"""Tests for the health endpoint."""

import os
from unittest.mock import patch

import pytest
from httpx import ASGITransport, AsyncClient

TEST_ENVIRONMENT = {
    "API_V1_PREFIX": "/api/v1",
    "APP_ENV": "test",
    "APP_NAME": "Investment Platform API",
    "DATABASE_URL": "postgresql+psycopg://localhost/investment_platform_test",
    "DEBUG": "false",
}

with patch.dict(os.environ, TEST_ENVIRONMENT, clear=True):
    from app.main import app


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.anyio
async def test_health_endpoint() -> None:
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
