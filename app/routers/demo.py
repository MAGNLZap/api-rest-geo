from fastapi import APIRouter, Request
from fastapi.responses import FileResponse

router = APIRouter(tags=["demo"])

@router.get("/demo")
async def demo(request: Request):
    return FileResponse("demo/demo.html")

@router.get("/ua_amenazas")
async def demo_ua_amenazas(request: Request):
    return FileResponse("demo/ua_amenazas.html")