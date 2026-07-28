# Convenciones GeoJSON

## Estándar

Seguir RFC 7946 (GeoJSON).

## Formato de Coordenadas

Siempre `[longitude, latitude]` (NO `[lat, lng]`).

```json
[-73.9857, 40.7484]  // longitude, latitude
```

## Tipo Geométrico Disponible

El sistema usa únicamente `Point` para representar ubicaciones geográficas.

### Estructura de Respuesta

#### Single Feature

```json
{
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [-73.9857, 40.7484]
  },
  "properties": {
    "id": 1,
    "nombre": "Nombre de la unidad",
    "departamento": "Guayas",
    "ciudad": "Guayaquil",
    ...
  },
  "id": "1"
}
```

#### FeatureCollection (listado)

```json
{
  "type": "FeatureCollection",
  "features": [
    { "type": "Feature", "geometry": {...}, "properties": {...}, "id": "1" }
  ],
  "total": 1234,
  "limit": 50,
  "offset": 0
}
```

## Schemas Pydantic

En `app/schemas/unidad_atencion.py`:

- `Feature` — Feature GeoJSON con geometry Point + properties
- `FeatureCollection` — Colección de features con metadata de paginación
- `UnidadProperties` — Propiedades de la unidad de atención
- `UnidadRaw` — Formato JSON plano (sin GeoJSON wrapper)
- `UnidadRawList` — Lista de unidades en formato raw

## Al Crear Endpoints Geográficos

1. Usar schemas de `app/schemas/unidad_atencion.py`
2. Modelo en `app/models/unidad_atencion.py` con campos `longitude` y `latitude` como Float
3. Convertir modelo → Feature con helper `_unidad_to_feature()`
4. Respuesta de listado → `FeatureCollection`
5. Respuesta individual → `Feature`
6. Formato raw → `UnidadRaw` / `UnidadRawList`
