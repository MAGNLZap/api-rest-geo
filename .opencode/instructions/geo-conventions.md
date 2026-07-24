# Convenciones GeoJSON

## Estándar

Seguir RFC 7946 (GeoJSON).

## Formato de Coordenadas

Siempre `[longitude, latitude]` (NO `[lat, lng]`).

```json
[-73.9857, 40.7484]  // longitude, latitude
```

## Tipos Geométricos Disponibles

| Tipo | Coordenadas | Ejemplo |
|---|---|---|
| `Point` | `[lng, lat]` | `[-73.9857, 40.7484]` |
| `LineString` | `[[lng, lat], ...]` | Mínimo 2 puntos |
| `Polygon` | `[[[lng, lat], ...]]` | Anillos (exterior + interiores) |
| `MultiPoint` | `[[lng, lat], ...]` | Lista de puntos |
| `MultiLineString` | `[[[lng, lat], ...], ...]` | Lista de líneas |
| `MultiPolygon` | `[[[lng, lat], ...], ...]` | Lista de polígonos |

## Estructura de Respuesta

### Single Feature

```json
{
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [-73.9857, 40.7484]
  },
  "properties": {
    "id": 1,
    "name": "Nombre del punto",
    "description": "Descripción opcional",
    "category": "categoría"
  },
  "id": "1"
}
```

### FeatureCollection (listado)

```json
{
  "type": "FeatureCollection",
  "features": [
    { "type": "Feature", "geometry": {...}, "properties": {...}, "id": "1" }
  ]
}
```

## Schemas Pydantic Disponibles

En `app/schemas/geo.py`:

- `Point`, `LineString`, `Polygon`, `MultiPoint`, `MultiLineString`, `MultiPolygon`
- `Geometry` = unión de todos los tipos
- `Feature` (geometry + properties + id)
- `FeatureCollection` (features [])

## Al Crear Endpoints Geográficos

1. Usar schemas de `app/schemas/geo.py` para respuestas
2. Modelo en `app/models/point.py` con `longitude` y `latitude` como Float
3. Convertir modelo → Feature con helper `_point_to_feature()`
4. Respuesta de listado → `FeatureCollection`
5. Respuesta individual → `Feature`
