# ApiRestGeo — Setup y Contexto

## Requisitos
- Python 3.14+
- PowerShell (Windows)

## Crear y activar entorno virtual

```pwsh
python -m venv .venv
.venv\Scripts\activate
```

## Instalar dependencias

```pwsh
.venv\Scripts\activate
pip install -r requirements.txt
```

Para producción (PostgreSQL en Linux):
```pwsh
pip install -r requirements-prod.txt
```

## Variables de entorno

Copiar `.env.example` a `.env` y configurar:

| Variable | Default | Descripción |
|---|---|---|
| `ENVIRONMENT` | `development` | `development` o `production` |
| `DATABASE_URL` | `sqlite+aiosqlite:///./test.db` | SQLite dev / PostgreSQL prod |
| `ALLOWED_ORIGINS` | (vacío) | Orígenes CORS externos (separados por coma) |
| `ALLOW_LOCAL_NETWORK` | `true` | Permitir redes locales |
| `PORT` | `8001` | Puerto del servidor |

## Iniciar servidor

```pwsh
.venv\Scripts\activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

Endpoints:
- `http://localhost:8001/` — metadata
- `http://localhost:8001/docs` — Swagger UI
- `http://localhost:8001/redoc` — ReDoc

## Ejecutar tests

```pwsh
.venv\Scripts\activate
python -m pytest tests/ -v
```

## Estructura del proyecto

```
ApiRestGeo/
├── .venv/                    # Entorno virtual
├── .env                      # Variables de entorno (no commit)
├── requirements.txt          # Dependencias dev
├── requirements-prod.txt     # Dependencias prod (+ asyncpg)
├── opencode.jsonc            # Config opencode
├── tests/
│   ├── conftest.py           # Fixtures async
│   ├── test_health.py
│   └── test_geo.py
└── app/
    ├── main.py               # Entry point FastAPI
    ├── config.py             # Pydantic Settings
    ├── database.py           # Engine async SQLAlchemy
    ├── models/base.py        # Base declarativa
    ├── models/point.py       # GeoPoint
    ├── routers/health.py     # GET /, GET /health
    ├── routers/geo.py        # GET /geo/points
    ├── schemas/geo.py        # Schemas GeoJSON
    └── middleware/cors.py    # CORS dinámico
```
