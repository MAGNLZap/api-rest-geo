---
name: geo-endpoint
description: Crea endpoints geográficos con estándar GeoJSON
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: fastapi
---

## Qué hace

Crea endpoints REST que devuelven datos geográficos en formato GeoJSON (RFC 7946).

## Cuándo usarlo

Cuando el usuario pide:
- Crear un endpoint geográfico
- Agregar un punto/feature/featurecollection
- Cualquier cosa relacionada con datos espaciales o mapas

## Flujo

1. Crear modelo SQLAlchemy con `longitude` y `latitude` (Float)
2. Crear router con `APIRouter(prefix="/...", tags=["geo"])`
3. Implementar conversión modelo → Feature usando Point de `app/schemas/geo.py`
4. Respuestas: listado → FeatureCollection, individual → Feature
5. Registrar router en `app/main.py`

## Schemas disponibles

`app/schemas/geo.py` contiene: Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon, Geometry, Feature, FeatureCollection.

## Convenciones de coordenadas

Siempre `[longitude, latitude]` (lon primero, lat segundo).

## Ejemplo de Feature

```json
{
  "type": "Feature",
  "geometry": {"type": "Point", "coordinates": [-73.9857, 40.7484]},
  "properties": {"id": 1, "name": "Lugar"},
  "id": "1"
}
```
