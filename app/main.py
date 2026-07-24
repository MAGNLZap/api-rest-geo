from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.config import settings
from app.database import engine
from app.middleware.cors import setup_cors
from app.models.base import Base
from app.routers.health import router as health_router
from app.routers.geo import router as geo_router

# Importar modelos para que Base los registre
from app.models.point import GeoPoint  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="ApiRestGeo",
    description="API REST para información geográfica con estándar GeoJSON",
    version="0.1.0",
    docs_url="/docs" if settings.is_dev else None,
    redoc_url="/redoc" if settings.is_dev else None,
    lifespan=lifespan,
)

setup_cors(app)
app.include_router(health_router)
app.include_router(geo_router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=settings.is_dev)
