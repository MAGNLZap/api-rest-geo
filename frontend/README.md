# Presentación del geoportal

Vue 3 + TypeScript + Vite, con Leaflet. Es un consumidor de la API REST,
no su reemplazo. La API puede arrancar y atender otros sistemas sin Node
ni este frontend.

## Desarrollo con Docker Desktop (recomendado)

Desde la raíz del proyecto:

```powershell
docker compose --env-file .env -f compose.dev.yaml up -d --build
```

En Docker Desktop → **Containers** aparece el grupo **apirestgeo-dev**:

- `web`: Vue/Vite, http://127.0.0.1:5173/
- `api`: FastAPI, http://127.0.0.1:8001/docs

Los mapas están en `/unidades_infancia` y `/ua_amenazas` en el puerto 5173.
El navegador accede a la API mediante el proxy de Vite, sin CORS adicional.

La API lee directamente el `.env` existente mediante `env_file`.
**No se modifica ese archivo ni se sobrescribe `DATABASE_URL`.**
Se conecta al PostgreSQL/PostGIS externo configurado, con el esquema y
los datos ya existentes. No hay servidor de BD, volumen SQLite, cargas,
migraciones ni creación automática de tablas al arrancar.

Dentro de Docker, `localhost` identifica al contenedor, no al servidor de
BD. La dirección de tu PostgreSQL externo debe ser accesible desde Docker.
Los puertos de desarrollo se publican solo en loopback.

Los cambios de archivos se reflejan automáticamente: Vue usa HMR y
FastAPI recarga los módulos de `app/`. Se activa polling para los
montajes de Docker Desktop en Windows.

Como el arranque usa `-d`, **puedes cerrar la consola**. Desde Docker
Desktop puedes ver logs, detener e iniciar ambos servicios. Docker Desktop
debe permanecer funcionando.

```powershell
# Estado y logs
docker compose --env-file .env -f compose.dev.yaml ps
docker compose --env-file .env -f compose.dev.yaml logs -f

# Detener sin eliminar contenedores; iniciar de nuevo
docker compose --env-file .env -f compose.dev.yaml stop
docker compose --env-file .env -f compose.dev.yaml start

# Retirar los contenedores, sin tocar la BD externa
docker compose --env-file .env -f compose.dev.yaml down
```

Si cambias `package-lock.json`, actualiza el volumen de dependencias:

```powershell
docker compose --env-file .env -f compose.dev.yaml stop web
docker compose --env-file .env -f compose.dev.yaml run --rm --no-deps web npm ci
docker compose --env-file .env -f compose.dev.yaml up -d --build
```

## Alternativa sin Docker

Requiere Node 22.12+ (recomendado 24 LTS), Python y `.venv`. Instalar
dependencias con `npm --prefix frontend ci` y abrir dos terminales:

```powershell
.\scripts\dev.ps1 -Service api
.\scripts\dev.ps1 -Service web
```

Cada comando se ejecuta en una terminal distinta. El script usa la
conexión de `.env` sin sustituirla. No ejecutar esta alternativa a la vez
que Docker en los mismos puertos.

En Linux/macOS:

```bash
.venv/bin/python -m uvicorn scripts.dev_api:create_app --factory \
  --host 127.0.0.1 --port 8001 --reload --reload-dir app
# En otra terminal:
npm --prefix frontend run dev
```

La factoría local fija desarrollo y prefijo vacío. `DATABASE_URL` sigue
siendo obligatorio y proviene de `.env` o del entorno.

## Estructura

```text
src/
  views/                 Portada y plantillas Vue de ambos mapas
  components/MapLoading.vue
  features/
    leaflet.js           Instancia compartida para los plugins
    unidades/map.js      Lógica existente de Unidades
    amenazas/map.js      Lógica existente de Amenazas, conservada conjuntamente
    amenazas/diccionario.json
  services/api.ts        Direcciones públicas del portal y de la API
  styles/                Estilos trasladados, sin rediseño
```

Los recursos institucionales de `app/static/` y el patrón de `demo/`
se incorporan al compilar mediante alias; no se descargan desde la API
ni se duplican en otro árbol de fuentes.

Los controles cartográficos existentes siguen siendo imperativos dentro
de sus controladores. Vue monta las plantillas y el loader y se encarga
del ciclo de vida. Esto conserva comportamiento sin introducir una
reescritura de algoritmos en la misma entrega. Las futuras funcionalidades
de Unidades pueden añadirse como componentes Vue.

La navegación entre vistas usa enlaces completos deliberadamente:
mantiene el comportamiento anterior y evita mezclar estilos globales
de los dos mapas. No hay iframe, `v-html` ni scripts HTML inyectados.
ExcelJS y html2canvas se descargan solo al pedir una exportación.

## Compilación

```powershell
npm --prefix frontend run build
```

Genera `frontend/dist/`, que no se versiona. Ejecuta análisis TypeScript
y compila Vue, pero **no es una prueba funcional de los mapas**.

Configuración pública en tiempo de compilación:

| Variable | Desarrollo | Producción actual |
|---|---|---|
| `VITE_PUBLIC_BASE` | `/` | `/api-geo/` |
| `VITE_API_BASE` | vacío (mismo origen) | `/api-geo` |
| `API_PROXY_TARGET` | `http://127.0.0.1:8001` | solo desarrollo |

No incluir contraseñas ni tokens en `VITE_*`: se incorporan al JavaScript
público. Para cambiar el prefijo de producción hay que recompilar y
coordinarlo con Nginx y `ROOT_PATH`; cambiar solo el entorno del
contenedor web no modifica un build existente.

`npm run preview` sirve para inspeccionar los archivos compilados, no es
un servidor de producción ni dispone del proxy de desarrollo. Para
inspeccionar datos contra una API real usar Vite dev o Nginx configurado.

Ver [despliegue y reversión](../deploy/README.md).
