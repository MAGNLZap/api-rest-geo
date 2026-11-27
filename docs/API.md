# API y datos

## Contratos

Las rutas de producción se publican en `/`, sin prefijo:

| Ruta GET | Respuesta |
|---|---|
| `/health` | Estado de aplicación y conexión a BD |
| `/unidades` | GeoJSON FeatureCollection, filtros y clustering |
| `/unidades/raw` | JSON plano |
| `/unidades/{id}` | GeoJSON Feature |
| `/unidades/{id}/raw` | JSON plano |
| `/dpa/provincias` | GeoJSON gzip |
| `/dpa/cantones` | GeoJSON gzip |
| `/dpa/parroquias` | GeoJSON gzip |
| `/ua_amenazas/data` | GeoJSON de amenazas |

Coordenadas RFC 7946 `[longitude, latitude]`; DPA usa MultiPolygon y
propiedades estándar según nivel. Las rutas web `/`, `/servicios_sociales`,
`/unidades_infancia` y `/ua_amenazas` las sirve Vue en producción.
Swagger/ReDoc solo están habilitados en desarrollo, no en producción.

`/unidades` admite `limit` (100 por defecto, 0 para todos, máximo paginado
1000), `offset`, `region`, `provincia`, `canton`, `servicio`, `tipo`, `area`,
`nombre`, `bbox`, `cluster`, `grid_size` y `zoom`. `bbox` es
`min_lng,min_lat,max_lng,max_lat`; clustering requiere bbox.
Consultar OpenAPI en desarrollo para tipos y restricciones exactas.

## Preparación de BD

La distribución no incluye datos operativos de unidades ni amenazas.
Obtenerlos por un canal autorizado. Requiere PostgreSQL/PostGIS externo;
SQLite no es un backend de ejecución. El arranque de la API **no** crea
tablas, aplica migraciones ni importa filas.

Antes de operar una BD nueva, el administrador debe revisar los scripts
en `scripts/load_data.py` y `scripts/sql/`, sus permisos y el modelo de datos.
No son un instalador automático universal ni deben ejecutarse a ciegas sobre
una BD existente. Hay esquemas provisionales y alternativas documentadas;
elegir el esquema compatible con los routers actuales.

Para usar herramientas de datos en un entorno Python 3.12 aislado:

```bash
pip install -r requirements-data.txt
python scripts/load_data.py --help
```

Las herramientas leen la configuración privada del entorno o `.env`.
Revisar migración y carga por separado, con respaldo y aprobación del operador.
No poner credenciales en la línea de comandos, historial de shell o Git.

Las semillas DPA se encuentran en `data/seed/`; los tres artefactos
`app/data/*.json.gz` son necesarios para el arranque y ya se incluyen.
La exportación DPA desde la BD es una tarea explícita del administrador,
no parte del despliegue de contenedores.

El preparador histórico de amenazas requiere fuentes operativas externas
y un HTML fuente con datos embebidos que no se distribuye. No es necesario
para construir o ejecutar el geoportal; ver `data/seed/ua_amenazas.md`.

## Pruebas de aplicación con BD

Solo bajo solicitud expresa, con PostgreSQL exclusivo de pruebas:

```bash
python -m pytest tests/ -q
```

Requieren `TEST_DATABASE_URL` configurado **privadamente** con driver
`postgresql+asyncpg`, host explícito y nombre terminado en `_test`.
Las fixtures rechazan la base de la aplicación, crean un esquema aleatorio
por prueba y lo eliminan al terminar. Nunca usar la BD ni credenciales de
producción. Las pruebas de distribución sin BD están en `deploy/tests/`.
