import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import RedirectResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app import database
from app.config import VERSION, settings
from app.middleware.cors import setup_cors
from app.middleware.rate_limit import limiter
from app.models import UnidadAtencion  # noqa: F401
from app.models.base import Base
from app.routers.demo import router as demo_router
from app.routers.dpa import router as dpa_router
from app.routers.dpa import warmup_cache
from app.routers.health import router as health_router
from app.routers.ua_amenazas import router as ua_amenazas_router
from app.routers.unidad_atencion import router as unidad_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger.info("Starting ApiRestGeo API v%s [%s]", VERSION, settings.ENVIRONMENT)
    try:
        async with database.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created/verified")
        warmup_cache()
        yield
    finally:
        await database.engine.dispose()
        logger.info("Shutting down ApiRestGeo API")


app = FastAPI(
    root_path=settings.ROOT_PATH,
    title="ApiRestGeo",
    description="API REST para información geográfica",
    version=VERSION,
    docs_url="/docs" if settings.is_dev else None,
    redoc_url="/redoc" if settings.is_dev else None,
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=1000)

setup_cors(app)
app.include_router(health_router)
app.include_router(unidad_router)
app.include_router(demo_router)
app.include_router(dpa_router)
app.include_router(ua_amenazas_router)


@app.exception_handler(StarletteHTTPException)
async def handle_http_exception(request: Request, error: StarletteHTTPException):
    if error.status_code == 404 and "text/html" in request.headers.get("accept", ""):
        path = request.url.path
        root_path = request.scope.get("root_path", "")
        if root_path and path.startswith(root_path):
            path = path[len(root_path) :] or "/"
        api_paths = ("/health", "/unidades", "/dpa", "/ua_amenazas/data")
        if not any(path == prefix or path.startswith(f"{prefix}/") for prefix in api_paths):
            target = "/" if settings.is_dev else request.url_for("root")
            return RedirectResponse(target, status_code=302)
    return await http_exception_handler(request, error)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.is_dev,
        forwarded_allow_ips=settings.FORWARDED_ALLOW_IPS,
    )
