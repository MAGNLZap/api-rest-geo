from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.config import VERSION, settings
from app.database import engine
from app.middleware.cors import setup_cors
from app.models import UnidadAtencion  # noqa: F401
from app.models.base import Base
from app.routers.health import router as health_router
from app.routers.unidad_atencion import router as unidad_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="ApiRestGeo",
    description="API REST para información geográfica",
    version=VERSION,
    docs_url="/docs" if settings.is_dev else None,
    redoc_url="/redoc" if settings.is_dev else None,
    lifespan=lifespan,
)

setup_cors(app)
app.include_router(health_router)
app.include_router(unidad_router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.is_dev)
