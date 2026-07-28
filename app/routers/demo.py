from fastapi import APIRouter, Request
from fastapi.responses import FileResponse

router = APIRouter(tags=["demo"])

@router.get("/demo")
async def demo(request: Request):
    return FileResponse("demo/demo.html")
