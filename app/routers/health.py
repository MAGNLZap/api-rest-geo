from datetime import datetime, timezone

from fastapi import APIRouter

from app.config import settings
from app.database import check_db_connection

router = APIRouter(tags=["health"])

VERSION = "0.1.0"


@router.get("/")
def root():
    return {
        "message": "ApiRestGeo API v0.1.0",
        "version": VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "docs": "/docs",
        "environment": settings.ENVIRONMENT,
    }


@router.get("/health")
async def health():
    db_ok = await check_db_connection()
    return {
        "status": "healthy" if db_ok else "degraded",
        "version": VERSION,
        "database": "connected" if db_ok else "disconnected",
    }
