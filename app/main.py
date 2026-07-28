from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
import logging

import uvicorn
from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.config import VERSION, settings
from app.database import engine
from app.middleware.cors import setup_cors
from app.middleware.rate_limit import limiter
from app.models import UnidadAtencion  # noqa: F401
from app.models.base import Base
from app.routers.health import router as health_router
from app.routers.unidad_atencion import router as unidad_router
from app.routers.demo import router as demo_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger.info("Starting ApiRestGeo API v%s [%s]", VERSION, settings.ENVIRONMENT)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created/verified")
    yield
    logger.info("Shutting down ApiRestGeo API")


app = FastAPI(
    title="ApiRestGeo",
    description="API REST para información geográfica",
    version=VERSION,
    docs_url="/docs" if settings.is_dev else None,
    redoc_url="/redoc" if settings.is_dev else None,
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

setup_cors(app)
app.include_router(health_router)
app.include_router(unidad_router)
app.include_router(demo_router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.is_dev)
