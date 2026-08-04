import json
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/dpa", tags=["dpa"])

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

DPA_FILES = {
    "provincias": "provincias_6dec.json",
    "cantones": "cantones_6dec.json",
    "parroquias": "parroquias_6dec.json",
}

_cache: dict[str, dict] = {}


def _load_geojson(name: str) -> dict:
    if name in _cache:
        return _cache[name]
    path = DATA_DIR / DPA_FILES[name]
    if not path.is_file():
        raise HTTPException(status_code=404, detail="Recurso no encontrado")
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Archivo GeoJSON inválido")
    _cache[name] = data
    return data


@router.get("/provincias")
async def get_provincias(request: Request):
    return JSONResponse(
        content=_load_geojson("provincias"),
        media_type="application/geo+json",
    )


@router.get("/cantones")
async def get_cantones(request: Request):
    return JSONResponse(
        content=_load_geojson("cantones"),
        media_type="application/geo+json",
    )


@router.get("/parroquias")
async def get_parroquias(request: Request):
    return JSONResponse(
        content=_load_geojson("parroquias"),
        media_type="application/geo+json",
    )
