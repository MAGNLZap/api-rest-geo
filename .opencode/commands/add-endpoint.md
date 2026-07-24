---
description: Crea un router con endpoints CRUD GeoJSON
agent: build
---

Crea un nuevo router con endpoints geográficos.

Uso: `/add-endpoint <nombre> [modelo]`

Ejemplo: `/add-endpoint places Place`

## Pasos

1. Crear router en `app/routers/<nombre>.py`:
   - `APIRouter(prefix="/<nombre>", tags=["<nombre>"])`
   - Helper `_point_to_feature()` para convertir modelo → Feature
   - `GET /<nombre>` → listado como FeatureCollection
   - `GET /<nombre>/{id}` → individual como Feature

2. Registrar router en `app/main.py` con `app.include_router()`

3. Crear schema Pydantic si es necesario en `app/schemas/<nombre>.py`

## Template del Router

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.<modelo> import <Modelo>
from app.schemas.geo import Feature, FeatureCollection, Point

router = APIRouter(prefix="/<nombre>", tags=["<nombre>"])


def _point_to_feature(p) -> Feature:
    return Feature(
        geometry=Point(coordinates=(p.longitude, p.latitude)),
        properties={"id": p.id, "name": p.name},
        id=str(p.id),
    )


@router.get("", response_model=FeatureCollection)
async def list_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(<Modelo>))
    items = result.scalars().all()
    return FeatureCollection(features=[_point_to_feature(i) for i in items])


@router.get("/{item_id}", response_model=Feature)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(<Modelo>).where(<Modelo>.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="No encontrado")
    return _point_to_feature(item)
```
