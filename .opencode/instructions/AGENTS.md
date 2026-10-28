# ApiRestGeo

FastAPI con Python 3.12, SQLAlchemy async, Pydantic v2, SQLite en desarrollo y PostgreSQL/PostGIS en producción.

## Comandos

```pwsh
pip install -r requirements-dev.txt
python -m app.main
python -m ruff check app scripts tests
python -m pytest tests/ -q   # solo bajo petición explícita del usuario
```

La configuración está en `.env`; usar `.env.example` como referencia. Nunca exponer ni commitear credenciales.

## Arquitectura

- `app/main.py`: aplicación, lifespan, middleware y routers.
- `app/database.py`: engine, sesiones y health check.
- `app/models`, `app/schemas`, `app/routers`: capas de datos y API.
- `scripts/load_data.py`: migraciones y carga/exportación DPA.
- `data/seed`: semilla DPA; `app/data/*.json.gz`: artefactos web generados.

## Reglas

- Usar type hints y `async/await` para acceso a base de datos.
- Mantener configuración en `app/config.py` y DI con `Depends(get_db)`.
- Preferir el cambio correcto más pequeño; no añadir abstracciones ni compatibilidad sin necesidad concreta.
- No modificar cambios ajenos ni `.env`. Evitar comentarios salvo lógica no evidente.
- No ejecutar pruebas automatizadas por defecto. El usuario realiza normalmente la validación manual.
- Ejecutar pruebas solo cuando el usuario las solicite explícitamente. Para cambios complejos o de alto riesgo (BD, migraciones, seguridad, middleware o despliegue), explicar primero qué pruebas se recomiendan y esperar su aprobación.
- No añadir pruebas, usar agentes revisores ni crear planes extensos para cambios triviales.

## GeoJSON

- Seguir RFC 7946 y coordenadas `[longitude, latitude]`.
- Unidades de atención usan `Point` y los schemas de `app/schemas/unidad_atencion.py`.
- DPA usa `MultiPolygon`, cuatro decimales y propiedades `id`, `name`, `province_id`, `canton_id` según el nivel.
- Listados geográficos usan `FeatureCollection`; elementos individuales usan `Feature`.

## Seguridad

- Docs solo en development; CORS y rate limit se configuran por entorno.
- No ejecutar comandos destructivos, migraciones con limpieza, commits o despliegues sin petición explícita.
