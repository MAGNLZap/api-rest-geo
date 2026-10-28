# ApiRestGeo

API REST para información geográfica con unidades de atención. Sirve datos GeoJSON de ubicaciones de servicios de desarrollo infantil en Ecuador, con límites DPA (División Político-Administrativa) y clustering.

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

# Desarrollo, pruebas y scripts de datos
pip install -r requirements-dev.txt
```

Para ejecutar únicamente la API se usa `requirements.txt`. Los scripts de carga y exportación requieren `requirements-data.txt`.

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
| `ROOT_PATH` | `/api-geo` | Prefijo del reverse proxy; usar vacío si no aplica |
| `FORWARDED_ALLOW_IPS` | `127.0.0.1` | IP/red confiable del proxy para identificar clientes reales |
| `RATE_LIMIT_ENABLED` | `true` | Habilitar rate limiting |
| `RATE_LIMIT_STORAGE` | `memory://` | Backend: `memory://` o `redis://host:port` |
| `RATE_LIMIT` | `120/minute` | Límite global de requests por IP |
| `LOG_LEVEL` | `INFO` | Nivel de log: DEBUG, INFO, WARNING, ERROR, CRITICAL |

## Ejecutar

```bash
python -m app.main
```

**Nota:** La API usa `root_path=/api-geo` para reverse proxies. Detrás de un proxy, configurar la ruta base en el proxy (nginx `location /api-geo/`). En desarrollo local, acceder directamente en `http://localhost:8001`.

## Docker

```bash
# Build image
docker build -t apirestgeo .

# Run container
docker run -p 8001:8001 -e DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db apirestgeo

```

La imagen instala solo dependencias de ejecución, usa el usuario no-root `app` e incluye un `HEALTHCHECK`. Los tres artefactos DPA comprimidos se incorporan durante el build.

## Cargar datos

```bash
python scripts/load_data.py --file "data/06_ua_validadas_0626 (1).json"
python scripts/load_data.py --file "data/06_ua_validadas_0626 (1).json" --clear  # limpiar antes
```

## Datos DPA

La base de datos es la fuente principal de provincias, cantones y parroquias. Los GeoJSON de `data/seed/` se usan únicamente para la carga inicial. `app/data/` contiene solo los artefactos `.json.gz` generados desde la base de datos y servidos por la API.

```bash
python scripts/load_data.py migrate
python scripts/load_data.py dpa --clear
python scripts/load_data.py dpa-export
python scripts/load_data.py dpa-export --level parroquias
```

El export genera GeoJSON RFC 7946 comprimido, con cuatro decimales y propiedades estándar (`id`, `name`, `province_id`, `canton_id`). La escritura es atómica y determinista, y conserva una copia `.bak` temporal del artefacto anterior. No genera JSON plano en `app/data/`.

## Endpoints

| Método | Ruta | Content-Type | Descripción |
|---|---|---|---|
| `GET` | `/` | HTML | Portada del geoportal con acceso a los mapas |
| `GET` | `/health` | JSON | Estado de la API + conexión a BD |
| `GET` | `/ua_amenazas` | HTML | Mapa de amenazas conectado a la API |
| `GET` | `/unidades_infancia` | HTML | Mapa de unidades de atención |
| `GET` | `/portal/assets/{asset_name}` | SVG | Miniaturas geográficas de la portada |
| `GET` | `/ua_amenazas/data` | `application/geo+json` | Dataset completo UA-Amenazas; admite filtros y bbox |
| `GET` | `/unidades` | `application/geo+json` | Unidades (GeoJSON FeatureCollection, con clustering) |
| `GET` | `/unidades/raw` | JSON | Unidades (JSON plano, sin GeoJSON wrapper) |
| `GET` | `/unidades/{id}` | `application/geo+json` | Unidad por ID (GeoJSON Feature) |
| `GET` | `/unidades/{id}/raw` | JSON | Unidad por ID (JSON plano) |
| `GET` | `/dpa/provincias` | `application/geo+json` (gzip) | Límites de provincias (comprimido) |
| `GET` | `/dpa/cantones` | `application/geo+json` (gzip) | Límites de cantones (comprimido) |
| `GET` | `/dpa/parroquias` | `application/geo+json` (gzip) | Límites de parroquias (comprimido) |
| `GET` | `/docs` | HTML | Swagger UI (solo en development) |
| `GET` | `/redoc` | HTML | ReDoc (solo en development) |

El mapa de amenazas solicita el dataset completo una vez para conservar los filtros, estadísticas, selección poligonal y exportación Excel. Los filtros DPA usan códigos oficiales como texto, sin FK; los polígonos se solicitan a `/dpa/*`.

Las rutas web HTML inexistentes redirigen a `/`; las rutas de API desconocidas conservan su respuesta `404` JSON.

### Filtros disponibles en `/unidades`

| Parámetro | Tipo | Default | Descripción |
|---|---|---|---|
| `limit` | int | 100 | Registros por página (max: 1000). Usar `limit=0` para todos |
| `offset` | int | 0 | Offset para paginación |
| `region` | string | - | Filtrar por región (búsqueda parcial, case-insensitive) |
| `provincia` | string | - | Filtrar por provincia (búsqueda parcial) |
| `canton` | string | - | Filtrar por cantón (búsqueda parcial) |
| `servicio` | string | - | Filtrar por tipo de servicio |
| `tipo` | string | - | Filtrar por tipo (INTRAMURAL/EXTRAMURAL) |
| `area` | string | - | Filtrar por área (Urbano/Rural) |
| `nombre` | string | - | Buscar por nombre (búsqueda parcial) |
| `bbox` | string | - | Bounding box: `min_lng,min_lat,max_lng,max_lat` |
| `cluster` | bool | false | Activar clustering server-side (requiere `bbox`) |
| `grid_size` | int | 8 | Tamaño de celda para clustering (2-32) |
| `zoom` | int | - | Nivel de zoom para auto-ajustar `grid_size` (0-19) |

### Filtros en `/unidades/raw`

Mismos filtros disponibles (excepto `cluster`, `grid_size`, `zoom`), retorna JSON plano sin envoltorio GeoJSON.

### Exportar mapa completo

```
GET /unidades?bbox=-81.1,-4.9,-75.0,1.5&limit=0
```

Retorna todas las unidades dentro del bounding box sin paginación.

### Clustering server-side

El clustering se activa con `cluster=true` y un `bbox`. Usa SQL window functions para agrupar puntos en una grilla:

| Zoom | Grid size |
|---|---|
| 0-5 | 4 |
| 6-8 | 8 |
| 9-11 | 12 |
| 12-14 | 16 |
| 15-19 | 20 |

Cada celda retorna el punto más cercano al centro con `cluster_count` y `cell_id` en las propiedades.

## Mapa de unidades de atención

Acceder en `http://localhost:8001/unidades_infancia`. Mapa Leaflet con:

- **Base:** Google Maps tiles, centrado en Ecuador (zoom 6-20)
- **Markers:** Supercluster para clustering client-side (radius: 80, maxZoom: 14)
- **DPA:** 3 niveles (Provincias/Cantones/Parroquias) con colores por región:
  - Costa: `#FFCD56`
  - Sierra: `#5C9EFF`
  - Amazonía: `#FF6978`
  - Galápagos: `#18B2A2`
- **Hover:** Resalta polígono (fillOpacity 0.75), muestra nombre en leyenda
- **Click:** Zoom al polígono (fitBounds, maxZoom: 14)
- **Outline:** Borde blanco de Ecuador (weight: 9, smoothFactor: 1)
- **Popups:** Nombre, RUC, modalidad, servicio, provincia, cantón, área, tipo, dirigido a
- **Topbar:** Pills flotantes estilo Uber con backdrop-filter:blur, loading bar

## Rate Limiting

- Global: 120 requests/minute por IP (configurable vía `RATE_LIMIT`)
- Storage: memoria por defecto, Redis para producción (`RATE_LIMIT_STORAGE`)
- Deshabilitar: `RATE_LIMIT_ENABLED=false`

## Tests

```bash
python -m pytest tests/ -v
```

27 tests en total: 3 de health/arranque + 20 de unidades + 4 de DPA. Configuración en `pyproject.toml`:
- `asyncio_mode = "auto"` (pytest-asyncio)
- `testpaths = ["tests"]`
- Base de datos SQLite en memoria, recreada automáticamente por cada test

## Estructura del proyecto

```
ApiRestGeo/
├── .venv/                    # Entorno virtual
├── .env                      # Variables de entorno (no commitear)
├── .env.example              # Template de variables de entorno
├── pyproject.toml            # Metadata del proyecto, ruff, pytest
├── requirements.txt          # Dependencias de ejecución
├── requirements-data.txt     # Dependencias para scripts geográficos
├── requirements-dev.txt      # Dependencias de desarrollo y pruebas
├── Dockerfile                # Imagen de producción
├── data/                     # Archivos de datos crudos
├── demo/
│   ├── index.html            # Portada con acceso a los mapas
│   ├── ua_amenazas.html      # Mapa de amenazas conectado a FastAPI
│   └── unidades_infancia.html # Mapa de unidades de atención
├── scripts/
│   ├── load_data.py          # Migraciones, carga y exportación de datos
│   ├── prepare_ua_amenazas_import.py # Prepara CSV homologado sin cargar la BD
│   └── build_geoportal_previews.py # Genera miniaturas con DPA y puntos
├── scripts/sql/              # Migraciones DPA y esquema provisional UA-Amenazas
├── data/seed/                # Semilla DPA inicial (GeoJSON estándar, 4 decimales)
├── app/
│   ├── main.py               # Entry point FastAPI, lifespan, GZipMiddleware
│   ├── config.py             # Configuración con Pydantic Settings
│   ├── database.py           # Engine async SQLAlchemy, session, get_db()
│   ├── data/                 # Artefactos DPA generados desde la base
│   │   ├── provincias.json.gz
│   │   ├── cantones.json.gz
│   │   └── parroquias.json.gz
│   ├── static/ua_amenazas/   # Logo y banner de reportes
│   ├── static/portal/        # Miniaturas geográficas de la portada
│   ├── middleware/
│   │   ├── cors.py           # CORS dinámico (auto-detecta IP local)
│   │   └── rate_limit.py     # Rate limiting (slowapi, per-IP)
│   ├── models/
│   │   ├── __init__.py       # Registro de modelos
│   │   ├── base.py           # Base declarativa SQLAlchemy
│   │   └── unidad_atencion.py # Modelo UnidadAtencion (39 campos, 7 índices)
│   ├── routers/
│   │   ├── health.py         # GET /, GET /health
│   │   ├── unidad_atencion.py # GET /unidades, /raw, /{id}, /{id}/raw
│   │   ├── demo.py           # Rutas de mapas y recursos estáticos
│   │   ├── dpa.py            # GET /dpa/provincias, /cantones, /parroquias
│   │   └── ua_amenazas.py    # GET /ua_amenazas/data
│   └── schemas/
│       └── unidad_atencion.py # Schemas Pydantic + GeoJSON (Feature, FeatureCollection)
└── tests/
    ├── conftest.py           # Fixtures async, client, test DB
    ├── test_dpa.py           # Tests de endpoints DPA comprimidos
    ├── test_health.py        # Tests de health endpoints
    └── test_unidades.py      # Tests de endpoints de unidades (20 tests)
```

## Base de datos

- **Desarrollo:** SQLite async (`sqlite+aiosqlite:///./test.db`, se crea automáticamente al iniciar)
- **Producción:** PostgreSQL/PostGIS async (`postgresql+asyncpg://...`, incluido en `requirements.txt`)
- **Modelo:** `UnidadAtencion` con 39 campos y 7 índices (incluyendo compuesto `longitude, latitude`)
- **Tests:** Base de datos SQLite en memoria, recreada para cada test

## Cache DPA

Los endpoints DPA (`/dpa/*`) sirven archivos `.gz` pre-comprimidos directamente desde memoria:

- `warmup_cache()` carga los 3 archivos `.gz` en un diccionario en memoria al iniciar el servidor
- Respuestas con `Content-Encoding: gzip` y `Cache-Control: public, max-age=3600`
- Rendimiento: ~8ms con cache caliente vs ~5s sin optimización
- GZipMiddleware de FastAPI se aplica a otras respuestas (> 1KB)

## Código de calidad

Configurado en `pyproject.toml`:

```bash
# Linting
ruff check app scripts tests

# Formatting
ruff format app scripts tests
```

- **Ruff:** `line-length=120`, target `py312`, reglas: `E`, `F`, `I`, `UP`
- **Python:** `>=3.12` con type hints en todos los métodos

## Seguridad

- CORS habilitado para redes locales por defecto (auto-detecta IP local vía UDP socket)
- Orígenes externos se configuran vía `ALLOWED_ORIGINS` en `.env`
- Documentación (Swagger/ReDoc) solo disponible en modo `development`
- Rate limiting global habilitado por defecto (120 req/min por IP)
- En despliegues con reverse proxy, configurar `FORWARDED_ALLOW_IPS` con la IP o red del proxy
- Storage de rate limiting configurable: memoria (`memory://`) o Redis (`redis://host:port`)
- GZipMiddleware habilitado para respuestas > 1KB
- Nunca commitear archivos `.env` con credenciales

## Licencia

Proyecto privado.
