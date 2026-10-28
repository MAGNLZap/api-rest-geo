---
name: geo-endpoint
description: Use when creating or modifying GeoJSON, map, Point, MultiPolygon, DPA, or geographic FastAPI endpoints in ApiRestGeo.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: fastapi
---

# Endpoints GeoJSON

Inspecciona primero el router y schema existente más cercano. Implementa el cambio mínimo con FastAPI, SQLAlchemy async y Pydantic v2.

## Convenciones

- Seguir RFC 7946 y usar `[longitude, latitude]`.
- Unidades de atención: `Point` y schemas de `app/schemas/unidad_atencion.py`.
- DPA: `MultiPolygon`, cuatro decimales y propiedades `id`, `name`, `province_id`, `canton_id` según el nivel.
- Listados: `FeatureCollection`; elementos: `Feature`.

## Flujo

1. Reutiliza schemas existentes; crea uno nuevo solo si el contrato cambia.
2. Usa `Depends(get_db)` y consultas async para datos dinámicos.
3. Registra routers nuevos en `app/main.py`.
4. Respeta filtros, paginación y formato existentes.
5. Describe la validación manual. Ejecuta tests solo por petición explícita o aprobación del usuario.
