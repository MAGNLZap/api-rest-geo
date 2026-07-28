from datetime import datetime, timezone

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.config import VERSION, settings
from app.database import check_db_connection

router = APIRouter(tags=["health"])


@router.get("/")
def root(request: Request):
    response = {
        "message": f"ApiRestGeo API v{VERSION}",
        "version": VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "environment": settings.ENVIRONMENT,
    }
    if settings.is_dev:
        response["docs"] = "/docs"
    return response


@router.get("/health")
async def health(request: Request):
    db_ok = await check_db_connection()
    status_code = 200 if db_ok else 503
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "healthy" if db_ok else "degraded",
            "version": VERSION,
            "database": "connected" if db_ok else "disconnected",
        },
    )
