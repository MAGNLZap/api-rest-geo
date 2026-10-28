import pytest
from slowapi.middleware import SlowAPIMiddleware

from app.main import app, lifespan


@pytest.mark.asyncio
async def test_root(client):
    response = await client.get("/")
    assert response.status_code == 302
    assert response.headers["location"] == "/ua_amenazas"


@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"


@pytest.mark.asyncio
async def test_application_lifespan() -> None:
    async with lifespan(app):
        assert app.state.limiter.enabled
        assert any(middleware.cls is SlowAPIMiddleware for middleware in app.user_middleware)
