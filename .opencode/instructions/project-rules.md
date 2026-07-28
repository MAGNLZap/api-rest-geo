# Reglas del Proyecto ApiRestGeo

## Estructura del Proyecto

```
ApiRestGeo/
├── app/
│   ├── config.py           # Settings con pydantic-settings, lee .env
│   ├── database.py         # Engine async, session, get_db()
│   ├── main.py             # Entry point FastAPI, lifespan, routers
│   ├── middleware/
│   │   ├── cors.py         # CORS dinámico (local + ALLOWED_ORIGINS)
│   │   └── rate_limit.py   # Rate limiting global (slowapi)
│   ├── models/
│   │   ├── __init__.py     # Registro de modelos
│   │   ├── base.py         # Base SQLAlchemy (DeclarativeBase)
│   │   └── unidad_atencion.py # Modelo UnidadAtencion (40+ campos)
│   ├── routers/
│   │   ├── health.py       # GET /, GET /health
│   │   └── unidad_atencion.py # GET /unidades, /raw, /{id}, /{id}/raw
│   └── schemas/
│       └── unidad_atencion.py # Schemas Pydantic (GeoJSON + Raw)
├── tests/
│   ├── conftest.py         # Fixtures async, client, test DB
│   ├── test_health.py      # Tests de health
│   └── test_unidades.py    # Tests de unidades (18+ tests)
```

## Convenciones de Código

- **Python 3.12** con type hints en todos los métodos
- **async/await** en toda capa de BD (SQLAlchemy async, aiosqlite, asyncpg)
- **Pydantic v2** para schemas (modelos de request/response)
- **Pydantic Settings** para configuración (.env)
- Sin comentarios en código a menos que el usuario los solicite explícitamente

## Base de Datos

- **Dev:** SQLite (`sqlite+aiosqlite:///./test.db`)
- **Prod:** PostgreSQL (`postgresql+asyncpg://...`) — requiere `requirements-prod.txt`
- Engine y session se crean en `app/database.py`
- Dependency injection con `Depends(get_db)` en los routers
- Tablas se crean automáticamente al iniciar (`Base.metadata.create_all`)

## Organización de Código

- Cada modelo en `app/models/<nombre>.py` con `__tablename__` explícito
- Cada router en `app/routers/<nombre>.py` con `APIRouter` y prefijo
- Schemas en `app/schemas/<nombre>.py` (Pydantic models)
- Registrar routers en `app/main.py` con `app.include_router()`
- Configuración centralizada en `app/config.py`

## Seguridad

- CORS: redes locales habilitadas por defecto
- Orígenes externos se configuran vía `ALLOWED_ORIGINS` en `.env`
- Docs/Redoc solo disponibles en modo `development`
- Rate limiting: 120 requests/minute por IP (configurable vía `RATE_LIMIT`)
- Nunca commitear `.env` ni archivos con credenciales
