# ApiRestGeo

API REST para información geográfica con estándar GeoJSON.

## Requisitos

- Python 3.14+
- pip

## Instalación

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd ApiRestGeo

# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# Windows (PowerShell):
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Variables de entorno

Copiar `.env.example` a `.env` y configurar según necesidad:

```bash
cp .env.example .env
```

| Variable | Default | Descripción |
|---|---|---|
| `ENVIRONMENT` | `development` | `development` o `production` |
| `DATABASE_URL` | `sqlite+aiosqlite:///./test.db` | SQLite dev / PostgreSQL prod |
| `ALLOWED_ORIGINS` | (vacío) | Orígenes CORS externos (separados por coma) |
| `ALLOW_LOCAL_NETWORK` | `true` | Permitir acceso desde redes locales |
| `PORT` | `8001` | Puerto del servidor |

## Ejecutar

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/` | Metadata de la API |
| `GET` | `/health` | Estado de la API + conexión a BD |
| `GET` | `/geo/points` | Todos los puntos geográficos |
| `GET` | `/geo/points/{id}` | Punto por ID |
| `GET` | `/docs` | Swagger UI (solo en development) |
| `GET` | `/redoc` | ReDoc (solo en development) |

## Tests

```bash
python -m pytest tests/ -v
```

## Estructura del proyecto

```
ApiRestGeo/
├── .venv/                    # Entorno virtual
├── .env                      # Variables de entorno (no commitear)
├── .env.example              # Template de variables de entorno
├── requirements.txt          # Dependencias de desarrollo
├── requirements-prod.txt     # Dependencias de producción (+ asyncpg)
├── app/
│   ├── main.py               # Entry point FastAPI
│   ├── config.py             # Configuración con Pydantic Settings
│   ├── database.py           # Engine async SQLAlchemy
│   ├── middleware/
│   │   └── cors.py           # CORS dinámico
│   ├── models/
│   │   ├── base.py           # Base declarativa SQLAlchemy
│   │   └── point.py          # Modelo GeoPoint
│   ├── routers/
│   │   ├── health.py         # Endpoints de salud
│   │   └── geo.py            # Endpoints geográficos
│   └── schemas/
│       └── geo.py            # Schemas GeoJSON (RFC 7946)
└── tests/
    ├── conftest.py           # Fixtures y configuración de tests
    ├── test_health.py        # Tests de health endpoints
    └── test_geo.py           # Tests de endpoints geográficos
```

## Base de datos

- **Desarrollo:** SQLite (archivo `test.db`, se crea automáticamente)
- **Producción:** PostgreSQL (requiere `pip install -r requirements-prod.txt`)

## Seguridad

- CORS habilitado para redes locales por defecto
- Orígenes externos se configuran vía `ALLOWED_ORIGINS` en `.env`
- Documentación (Swagger/ReDoc) solo disponible en modo `development`
- Nunca commitear archivos `.env` con credenciales

## Licencia

Proyecto privado.
