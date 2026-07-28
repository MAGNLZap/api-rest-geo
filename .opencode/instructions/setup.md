# ApiRestGeo — Setup y Contexto

## Requisitos
- Python 3.12+
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
| `HOST` | `0.0.0.0` | Host del servidor |
| `PORT` | `8001` | Puerto del servidor |
| `RATE_LIMIT_ENABLED` | `true` | Habilitar rate limiting |
| `RATE_LIMIT_STORAGE` | `memory://` | Backend: `memory://` o `redis://host:port` |
| `RATE_LIMIT` | `120/minute` | Límite global de requests |

## Iniciar servidor

```pwsh
.venv\Scripts\activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

Endpoints:
- `http://localhost:8001/` — metadata
- `http://localhost:8001/docs` — Swagger UI (solo development)
- `http://localhost:8001/redoc` — ReDoc (solo development)

## Cargar datos

```pwsh
python scripts/load_data.py --file "data/archivo.json"
python scripts/load_data.py --file "data/archivo.json" --clear  # limpiar antes
```

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
├── .env.example              # Template de variables
├── requirements-base.txt     # Dependencias compartidas
├── requirements.txt          # Dependencias dev (+ test)
├── requirements-prod.txt     # Dependencias prod (+ asyncpg)
├── data/                     # Archivos de datos (JSON, Excel)
├── scripts/
│   └── load_data.py          # Carga masiva JSON → SQLite
├── app/
│   ├── main.py               # Entry point FastAPI
│   ├── config.py             # Settings con pydantic-settings
│   ├── database.py           # Engine async, session, get_db()
│   ├── models/
│   │   ├── __init__.py       # Registro de modelos
│   │   ├── base.py           # Base SQLAlchemy (DeclarativeBase)
│   │   └── unidad_atencion.py # Modelo UnidadAtencion (40+ campos)
│   ├── routers/
│   │   ├── health.py         # GET /, GET /health
│   │   └── unidad_atencion.py # GET /unidades, /raw, /{id}, /{id}/raw
│   ├── schemas/
│   │   └── unidad_atencion.py # Schemas GeoJSON + Raw
│   └── middleware/
│       ├── cors.py           # CORS dinámico
│       └── rate_limit.py     # Rate limiting (slowapi)
└── tests/
    ├── conftest.py           # Fixtures async
    ├── test_health.py        # Tests de health
    └── test_unidades.py      # Tests de unidades (18 tests)
```
