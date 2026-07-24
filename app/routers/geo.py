from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.point import GeoPoint
from app.schemas.geo import Feature, FeatureCollection, Point

router = APIRouter(prefix="/geo", tags=["geo"])


def _point_to_feature(p: GeoPoint) -> Feature:
    return Feature(
        geometry=Point(coordinates=(p.longitude, p.latitude)),
        properties={
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "category": p.category,
        },
        id=str(p.id),
    )


@router.get("/points", response_model=FeatureCollection)
async def list_points(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(GeoPoint))
    points = result.scalars().all()
    return FeatureCollection(features=[_point_to_feature(p) for p in points])


@router.get("/points/{point_id}", response_model=Feature)
async def get_point(point_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(GeoPoint).where(GeoPoint.id == point_id))
    point = result.scalar_one_or_none()
    if not point:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Punto no encontrado")
    return _point_to_feature(point)
