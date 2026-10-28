from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

router = APIRouter(prefix="/ua_amenazas", tags=["ua-amenazas"])

MONTHS = (
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
)


def _parse_bbox(value: str) -> tuple[float, float, float, float]:
    try:
        coordinates = tuple(float(part.strip()) for part in value.split(","))
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail="bbox debe ser min_lon,min_lat,max_lon,max_lat",
        ) from error
    if len(coordinates) != 4:
        raise HTTPException(
            status_code=400,
            detail="bbox debe contener cuatro valores: min_lon,min_lat,max_lon,max_lat",
        )
    min_lon, min_lat, max_lon, max_lat = coordinates
    if not (-180 <= min_lon < max_lon <= 180 and -90 <= min_lat < max_lat <= 90):
        raise HTTPException(status_code=400, detail="bbox fuera de rango o con limites invertidos")
    return min_lon, min_lat, max_lon, max_lat


@router.get("/data")
async def get_ua_amenazas_data(
    fecha_corte: date | None = None,
    province_id: str | None = None,
    canton_id: str | None = None,
    parish_id: str | None = None,
    servicio: str | None = None,
    modalidad: str | None = None,
    region: str | None = None,
    tipo_atencion: str | None = None,
    area: str | None = None,
    bbox: str | None = None,
    limit: int | None = Query(None, ge=1, le=10_000),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> JSONResponse:
    if fecha_corte is None:
        fecha_corte = (await db.execute(text("SELECT max(fecha_corte) FROM ua_amenazas"))).scalar_one_or_none()

    if fecha_corte is None:
        return JSONResponse(
            content={
                "type": "FeatureCollection",
                "features": [],
                "metadata": {
                    "fecha_corte": None,
                    "corte": None,
                    "total": 0,
                    "limit": limit,
                    "offset": offset,
                },
            },
            media_type="application/geo+json",
            headers={"Cache-Control": "public, max-age=300"},
        )

    filters = ["fecha_corte = :fecha_corte"]
    parameters: dict[str, object] = {"fecha_corte": fecha_corte}
    for field, value in (
        ("province_id", province_id),
        ("canton_id", canton_id),
        ("parish_id", parish_id),
        ("servicio", servicio),
        ("modalidad", modalidad),
        ("region", region),
        ("tipo_atencion", tipo_atencion),
        ("area", area),
    ):
        if value is not None:
            filters.append(f"{field} = :{field}")
            parameters[field] = value

    if bbox is not None:
        min_lon, min_lat, max_lon, max_lat = _parse_bbox(bbox)
        filters.append("geom && ST_MakeEnvelope(:min_lon, :min_lat, :max_lon, :max_lat, 4326)")
        parameters.update(
            min_lon=min_lon,
            min_lat=min_lat,
            max_lon=max_lon,
            max_lat=max_lat,
        )

    where_clause = " AND ".join(filters)
    total = (await db.execute(text(f"SELECT count(*) FROM ua_amenazas WHERE {where_clause}"), parameters)).scalar_one()

    query = (
        "SELECT id, "
        "to_jsonb(u) - 'id' - 'created_at' - 'updated_at' - 'geom' AS properties, "
        "ST_X(geom) AS longitude, ST_Y(geom) AS latitude "
        f"FROM ua_amenazas AS u WHERE {where_clause} "
        "ORDER BY id"
    )
    query_parameters = dict(parameters)
    if limit is not None:
        query += " LIMIT :limit OFFSET :offset"
        query_parameters.update(limit=limit, offset=offset)

    result = await db.execute(text(query), query_parameters)
    features = [
        {
            "type": "Feature",
            "id": str(row["id"]),
            "geometry": {
                "type": "Point",
                "coordinates": [row["longitude"], row["latitude"]],
            },
            "properties": row["properties"],
        }
        for row in result.mappings()
    ]
    cutoff_label = f"{MONTHS[fecha_corte.month - 1]} {fecha_corte.year}"

    return JSONResponse(
        content=jsonable_encoder(
            {
                "type": "FeatureCollection",
                "features": features,
                "metadata": {
                    "fecha_corte": fecha_corte.isoformat(),
                    "corte": cutoff_label,
                    "total": total,
                    "limit": limit,
                    "offset": offset,
                },
            }
        ),
        media_type="application/geo+json",
        headers={"Cache-Control": "public, max-age=300"},
    )
