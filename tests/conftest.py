import os
from collections.abc import AsyncIterator
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.engine import URL, make_url
from sqlalchemy.exc import ArgumentError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

import app.database as app_database
from app.database import get_db
from app.main import app
from app.models.base import Base


def _test_database_url() -> URL:
    value = os.environ.get("TEST_DATABASE_URL")
    if not value:
        raise pytest.UsageError("Configura TEST_DATABASE_URL con una base PostgreSQL exclusiva terminada en _test.")
    try:
        url = make_url(value)
    except (ArgumentError, ValueError):
        raise pytest.UsageError("TEST_DATABASE_URL no es una URL PostgreSQL válida.") from None
    if url.drivername != "postgresql+asyncpg" or not url.host or not (url.database or "").endswith("_test"):
        raise pytest.UsageError(
            "TEST_DATABASE_URL requiere postgresql+asyncpg, host explícito y base terminada en _test."
        )
    if set(url.query) - {"ssl"}:
        raise pytest.UsageError("TEST_DATABASE_URL no permite parámetros de conexión adicionales salvo ssl.")
    _, current_args = app_database.engine.dialect.create_connect_args(app_database.engine.url)
    if url.database == current_args.get("database"):
        raise pytest.UsageError("La base de pruebas debe ser distinta de la configurada para la aplicación.")
    return url


@pytest.fixture(autouse=True)
async def setup_database() -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    url = _test_database_url()
    schema = f"apirestgeo_test_{uuid4().hex}"
    admin_engine = create_async_engine(url, poolclass=NullPool)
    test_engine = create_async_engine(
        url,
        poolclass=NullPool,
        connect_args={"server_settings": {"search_path": schema}},
    )
    session_maker = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
    previous_engine = app_database.engine
    previous_overrides = app.dependency_overrides.copy()

    async def override_get_db() -> AsyncIterator[AsyncSession]:
        async with session_maker() as session:
            yield session

    created = False
    try:
        async with admin_engine.begin() as conn:
            await conn.execute(text(f'CREATE SCHEMA "{schema}"'))
        created = True
        app_database.engine = test_engine
        app.dependency_overrides[get_db] = override_get_db
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield session_maker
    finally:
        app_database.engine = previous_engine
        app.dependency_overrides.clear()
        app.dependency_overrides.update(previous_overrides)
        try:
            await test_engine.dispose()
            if created:
                async with admin_engine.begin() as conn:
                    await conn.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
        finally:
            await admin_engine.dispose()


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
