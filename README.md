# ApiRestGeo

API REST para información geográfica con unidades de atención.

## Requisitos

- Python 3.12+
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
| `HOST` | `0.0.0.0` | Host del servidor |
| `PORT` | `8001` | Puerto del servidor |

## Ejecutar

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

## Cargar datos

```bash
python scripts/load_data.py --file "data/06_ua_validadas_0626 (1).json"
```

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/` | Metadata de la API |
| `GET` | `/health` | Estado de la API + conexión a BD |
| `GET` | `/unidades` | Todas las unidades (GeoJSON FeatureCollection) |
| `GET` | `/unidades/{id}` | Unidad por ID |
| `GET` | `/docs` | Swagger UI (solo en development) |
| `GET` | `/redoc` | ReDoc (solo en development) |

### Filtros disponibles en `/unidades`

| Parámetro | Tipo | Descripción |
|---|---|---|
| `limit` | int | Registros por página (default: 100, max: 1000) |
| `offset` | int | Offset para paginación |
| `region` | string | Filtrar por región |
| `provincia` | string | Filtrar por provincia |
| `canton` | string | Filtrar por cantón |
| `servicio` | string | Filtrar por tipo de servicio |
| `tipo` | string | Filtrar por tipo (INTRAMURAL/EXTRAMURAL) |
| `area` | string | Filtrar por área (Urbano/Rural) |
| `nombre` | string | Buscar por nombre |

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
├── requirements-base.txt     # Dependencias base
├── requirements.txt          # Dependencias de desarrollo
├── requirements-prod.txt     # Dependencias de producción
├── data/                     # Archivos de datos
├── scripts/
│   └── load_data.py          # Script de carga masiva
├── app/
│   ├── main.py               # Entry point FastAPI
│   ├── config.py             # Configuración con Pydantic Settings
│   ├── database.py           # Engine async SQLAlchemy
│   ├── middleware/
│   │   └── cors.py           # CORS dinámico
│   ├── models/
│   │   ├── __init__.py       # Registro de modelos
│   │   ├── base.py           # Base declarativa SQLAlchemy
│   │   └── unidad_atencion.py # Modelo UnidadAtencion
│   ├── routers/
│   │   ├── health.py         # Endpoints de salud
│   │   └── unidad_atencion.py # Endpoints de unidades
│   └── schemas/
│       └── unidad_atencion.py # Schemas Pydantic + GeoJSON
└── tests/
    ├── conftest.py           # Fixtures y configuración de tests
    ├── test_health.py        # Tests de health endpoints
    └── test_unidades.py      # Tests de endpoints de unidades
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
