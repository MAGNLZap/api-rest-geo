from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter(tags=["demo"])
UA_AMENAZAS_ASSETS = Path(__file__).resolve().parent.parent / "static" / "ua_amenazas"
PORTAL_ASSETS = Path(__file__).resolve().parent.parent / "static" / "portal"
TOPOGRAPHIC_PATTERN = Path(__file__).resolve().parents[2] / "demo" / "patron-topografico.svg"


@router.get("/ua_amenazas")
async def demo_ua_amenazas() -> FileResponse:
    return FileResponse("demo/ua_amenazas.html")


@router.get("/unidades_infancia")
async def unidades_infancia() -> FileResponse:
    return FileResponse("demo/unidades_infancia.html")


@router.get("/ua_amenazas/assets/{asset_name}")
async def ua_amenazas_asset(asset_name: str) -> FileResponse:
    if asset_name not in {"logo_encabezado.png", "banner_reporte.png"}:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")
    return FileResponse(UA_AMENAZAS_ASSETS / asset_name, media_type="image/png")


@router.get("/portal/assets/{asset_name}")
async def portal_asset(asset_name: str) -> FileResponse:
    if asset_name == "patron-topografico.svg":
        return FileResponse(TOPOGRAPHIC_PATTERN, media_type="image/svg+xml")
    if asset_name not in {
        "preview_unidades.svg",
        "preview_amenazas.svg",
        "ecuador_hero.svg",
        "topography_samples.svg",
        "header_grid.svg",
    }:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")
    return FileResponse(PORTAL_ASSETS / asset_name, media_type="image/svg+xml")
