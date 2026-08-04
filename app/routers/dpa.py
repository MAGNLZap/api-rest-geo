from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import Response

router = APIRouter(prefix="/dpa", tags=["dpa"])

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

DPA_FILES = {
    "provincias": "provincias_6dec.json.gz",
    "cantones": "cantones_6dec.json.gz",
    "parroquias": "parroquias_6dec.json.gz",
}

_cache: dict[str, bytes] = {}


def warmup_cache():
    for name in DPA_FILES:
        _load_geojson_raw(name)


def _load_geojson_raw(name: str) -> bytes:
    if name in _cache:
        return _cache[name]
    path = DATA_DIR / DPA_FILES[name]
    if not path.is_file():
        raise HTTPException(status_code=404, detail="Recurso no encontrado")
    raw = path.read_bytes()
    _cache[name] = raw
    return raw


@router.get("/provincias")
async def get_provincias(request: Request):
    return Response(
        content=_load_geojson_raw("provincias"),
        media_type="application/geo+json",
        headers={"Content-Encoding": "gzip", "Cache-Control": "public, max-age=3600"},
    )


@router.get("/cantones")
async def get_cantones(request: Request):
    return Response(
        content=_load_geojson_raw("cantones"),
        media_type="application/geo+json",
        headers={"Content-Encoding": "gzip", "Cache-Control": "public, max-age=3600"},
    )


@router.get("/parroquias")
async def get_parroquias(request: Request):
    return Response(
        content=_load_geojson_raw("parroquias"),
        media_type="application/geo+json",
        headers={"Content-Encoding": "gzip", "Cache-Control": "public, max-age=3600"},
    )
