from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse

from app.config import VERSION
from app.database import check_db_connection

router = APIRouter(tags=["health"])


@router.get("/")
def root() -> FileResponse:
    return FileResponse("demo/index.html")


@router.get("/health")
async def health() -> JSONResponse:
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
