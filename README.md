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
| `RATE_LIMIT_ENABLED` | `true` | Habilitar rate limiting |
| `RATE_LIMIT_STORAGE` | `memory://` | Backend: `memory://` o `redis://host:port` |
| `RATE_LIMIT` | `120/minute` | Límite global de requests por IP |
| `LOG_LEVEL` | `INFO` | Nivel de log: DEBUG, INFO, WARNING, ERROR, CRITICAL |

## Ejecutar

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

**Nota:** La API usa `root_path=/api-geo` para reverse proxies. Detrás de un proxy, configurar la ruta base en el proxy (nginx `location /api-geo/`). En desarrollo local, acceder directamente en `http://localhost:8001`.

## Docker

```bash
# Build image
docker build -t apirestgeo .

# Run container
docker run -p 8001:8001 -e DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db apirestgeo

# With volume for data files
docker run -p 8001:8001 -v ./app/data:/app/app/data -e DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db apirestgeo
```

El Dockerfile usa multi-stage build (builder + runtime) con usuario no-root `appuser`.

## Cargar datos

```bash
python scripts/load_data.py --file "data/06_ua_validadas_0626 (1).json"
python scripts/load_data.py --file "data/06_ua_validadas_0626 (1).json" --clear  # limpiar antes
```

## Optimizar datos DPA

Los archivos GeoJSON de la División Político-Administrativa (provincias, cantones, parroquias) requieren optimización antes de ser servidos por la API. El script reduce la precisión de coordenadas y genera archivos comprimidos.

```bash
python scripts/optimize_dpa.py
```

**Qué hace:**
1. Lee los archivos `.json` originales de `app/data/`
2. Reduce coordenadas de 14 decimales a 6 (~11cm de precisión)
3. Genera archivos `_6dec.json` (optimizados)
4. Genera archivos `_6dec.json.gz` (comprimidos con gzip nivel 9)

**Archivos generados:**

| Archivo original | Archivo optimizado | Archivo comprimido |
|---|---|---|
| `provincias.json` | `provincias_6dec.json` | `provincias_6dec.json.gz` |
| `cantones.json` | `cantones_6dec.json` | `cantones_6dec.json.gz` |
| `parroquias.json` | `parroquias_6dec.json` | `parroquias_6dec.json.gz` |

**Cuándo ejecutar:**
- Al actualizar los archivos GeoJSON DPA
- Al cambiar la precisión requerida (modificar `TARGET_DECIMALS` en el script)
- Después de clonar el repositorio por primera vez

**Nota:** Los archivos `.gz` son los que sirve la API. No eliminar los archivos `.json` originales (son fuente).

## Endpoints

| Método | Ruta | Content-Type | Descripción |
|---|---|---|---|
| `GET` | `/` | JSON | Metadata de la API (mensaje, versión, timestamp, environment, docs) |
| `GET` | `/health` | JSON | Estado de la API + conexión a BD |
| `GET` | `/demo` | HTML | Mapa demo interactivo (Leaflet + Supercluster + DPA) |
| `GET` | `/unidades` | `application/geo+json` | Unidades (GeoJSON FeatureCollection, con clustering) |
| `GET` | `/unidades/raw` | JSON | Unidades (JSON plano, sin GeoJSON wrapper) |
| `GET` | `/unidades/{id}` | `application/geo+json` | Unidad por ID (GeoJSON Feature) |
| `GET` | `/unidades/{id}/raw` | JSON | Unidad por ID (JSON plano) |
| `GET` | `/dpa/provincias` | `application/geo+json` (gzip) | Límites de provincias (comprimido) |
| `GET` | `/dpa/cantones` | `application/geo+json` (gzip) | Límites de cantones (comprimido) |
| `GET` | `/dpa/parroquias` | `application/geo+json` (gzip) | Límites de parroquias (comprimido) |
| `GET` | `/docs` | HTML | Swagger UI (solo en development) |
| `GET` | `/redoc` | HTML | ReDoc (solo en development) |

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

## Demo (Mapa interactivo)

Acceder en `http://localhost:8001/demo`. Mapa Leaflet con:

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

24 tests en total: 2 de health + 22 de unidades. Configuración en `pyproject.toml`:
- `asyncio_mode = "auto"` (pytest-asyncio)
- `testpaths = ["tests"]`
- Base de datos de test separada (`test_test.db`), se crea/destruye automáticamente por cada test

## Estructura del proyecto

```
ApiRestGeo/
├── .venv/                    # Entorno virtual
├── .env                      # Variables de entorno (no commitear)
├── .env.example              # Template de variables de entorno
├── pyproject.toml            # Metadata del proyecto, ruff, pytest
├── requirements.txt          # Dependencias
├── Dockerfile                # Imagen Docker multi-stage
├── data/                     # Archivos de datos crudos
│   └── 06_ua_validadas_0626 (1).json
├── demo/
│   └── demo.html             # Mapa interactivo (Leaflet + Supercluster + DPA)
├── scripts/
│   ├── load_data.py          # Script de carga masiva JSON → SQLite
│   └── optimize_dpa.py       # Optimización de archivos DPA (decimales + gzip)
├── app/
│   ├── main.py               # Entry point FastAPI, lifespan, GZipMiddleware
│   ├── config.py             # Configuración con Pydantic Settings
│   ├── database.py           # Engine async SQLAlchemy, session, get_db()
│   ├── data/                 # Datos DPA (GeoJSON)
│   │   ├── provincias.json       # Provincias (fuente, WGS84)
│   │   ├── provincias_6dec.json  # Provincias (optimizado)
│   │   ├── provincias_6dec.json.gz # Provincias (comprimido)
│   │   ├── cantones.json         # Cantones (fuente)
│   │   ├── cantones_6dec.json    # Cantones (optimizado)
│   │   ├── cantones_6dec.json.gz # Cantones (comprimido)
│   │   ├── parroquias.json       # Parroquias (fuente)
│   │   ├── parroquias_6dec.json  # Parroquias (optimizado)
│   │   └── parroquias_6dec.json.gz # Parroquias (comprimido)
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
│   │   ├── demo.py           # GET /demo (sirve demo.html)
│   │   └── dpa.py            # GET /dpa/provincias, /cantones, /parroquias
│   └── schemas/
│       └── unidad_atencion.py # Schemas Pydantic + GeoJSON (Feature, FeatureCollection)
└── tests/
    ├── conftest.py           # Fixtures async, client, test DB
    ├── test_health.py        # Tests de health endpoints
    └── test_unidades.py      # Tests de endpoints de unidades (22 tests)
```

## Base de datos

- **Desarrollo:** SQLite async (`sqlite+aiosqlite:///./test.db`, se crea automáticamente al iniciar)
- **Producción:** PostgreSQL async (`postgresql+asyncpg://...`, incluido en `requirements.txt`)
- **Modelo:** `UnidadAtencion` con 39 campos y 7 índices (incluyendo compuesto `longitude, latitude`)
- **Tests:** Base de datos SQLite separada (`test_test.db`), se crea/destruye por cada test

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
ruff check app/

# Formatting
ruff format app/
```

- **Ruff:** `line-length=120`, target `py312`, reglas: `E`, `F`, `I`, `UP`
- **Python:** `>=3.12` con type hints en todos los métodos

## Seguridad

- CORS habilitado para redes locales por defecto (auto-detecta IP local vía UDP socket)
- Orígenes externos se configuran vía `ALLOWED_ORIGINS` en `.env`
- Documentación (Swagger/ReDoc) solo disponible en modo `development`
- Rate limiting global habilitado por defecto (120 req/min por IP)
- Storage de rate limiting configurable: memoria (`memory://`) o Redis (`redis://host:port`)
- GZipMiddleware habilitado para respuestas > 1KB
- Nunca commitear archivos `.env` con credenciales

## Licencia

Proyecto privado.
