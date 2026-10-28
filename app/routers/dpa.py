import gzip
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import Response

router = APIRouter(prefix="/dpa", tags=["dpa"])

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

DPA_FILES = {
    "provincias": "provincias.json.gz",
    "cantones": "cantones.json.gz",
    "parroquias": "parroquias.json.gz",
}

_cache: dict[str, bytes] = {}


def warmup_cache() -> None:
    for name in DPA_FILES:
        _load_geojson_raw(name)


def _load_geojson_raw(name: str) -> bytes:
    if name in _cache:
        return _cache[name]
    path = DATA_DIR / DPA_FILES[name]
    if not path.is_file():
        raise RuntimeError(f"Falta el artefacto DPA requerido: {path}")
    raw = path.read_bytes()
    _cache[name] = raw
    return raw


def _response(name: str, request: Request) -> Response:
    compressed = _load_geojson_raw(name)
    qualities: dict[str, float] = {}
    for option in request.headers.get("accept-encoding", "").lower().split(","):
        parts = [part.strip() for part in option.split(";")]
        if not parts[0]:
            continue
        quality = 1.0
        for parameter in parts[1:]:
            if parameter.startswith("q="):
                try:
                    quality = float(parameter[2:])
                except ValueError:
                    quality = 0.0
        qualities[parts[0]] = quality

    headers = {"Cache-Control": "public, max-age=3600"}
    if qualities.get("gzip", qualities.get("*", 0.0)) > 0:
        headers["Content-Encoding"] = "gzip"
        content = compressed
    else:
        content = gzip.decompress(compressed)
    return Response(content=content, media_type="application/geo+json", headers=headers)


@router.get("/provincias")
async def get_provincias(request: Request) -> Response:
    return _response("provincias", request)


@router.get("/cantones")
async def get_cantones(request: Request) -> Response:
    return _response("cantones", request)


@router.get("/parroquias")
async def get_parroquias(request: Request) -> Response:
    return _response("parroquias", request)
