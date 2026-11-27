# Operación de geoportal-mtdh

Instalación inicial y variables: [INSTALL.md](INSTALL.md).
Ejecutar siempre desde la raíz del repositorio y usar `.env.production`.

## Estado y logs

```bash
docker compose --env-file .env.production ps
docker compose --env-file .env.production logs --tail=100 api web
```

No publicar logs sin revisarlos; pueden contener datos o errores de conexión.
El código se incorpora a las imágenes: editar archivos o hacer `git pull`
**no actualiza los contenedores activos**.

## Actualizar

1. Elegir una versión revisada del código y una ventana de mantenimiento.
2. Registrar la versión actual de Git y `IMAGE_TAG`; conservar sus imágenes
   y una copia privada de la configuración. No sobrescribir tags existentes.
3. Verificar que no hay cambios locales que puedan perderse. Obtener una
   versión publicada mediante `git fetch --tags` y seleccionar su tag real:

   ```bash
   git status --short
   git fetch --tags
   git checkout <TAG-DE-CODIGO-APROBADO>
   ```

4. Editar **solo `IMAGE_TAG`** en `.env.production` con una versión nueva.
   Revisar cambios de variables documentados, sin sobrescribir el archivo.
5. Construir y validar antes de reemplazar el servicio:

   ```bash
   docker compose --env-file .env.production config --quiet
   docker compose --env-file .env.production build
   ```

6. Si la construcción falla, **no ejecutar `up`**. Si pasa:

   ```bash
   docker compose --env-file .env.production up -d --no-build
   docker compose --env-file .env.production ps
   curl -f --max-time 10 http://127.0.0.1:18081/health
   ```

7. Esperar ambos servicios saludables y aceptar por el dominio público.
   Si cambió `WEB_PORT`, adaptar también el proxy; normalmente no se cambia.

La recreación puede causar una interrupción breve. Compose simple no es
un despliegue blue/green ni garantiza cero downtime o rollback automático.
No se ejecutan migraciones automáticas; cambios de esquema necesitan su
propio procedimiento, aprobación y respaldo de BD.

## Reversión

Restaurar la versión anterior de código/configuración y su `IMAGE_TAG`.
Ambas imágenes anteriores deben estar disponibles localmente:

```bash
docker compose --env-file .env.production config --quiet
docker compose --env-file .env.production up -d --no-build --pull never
docker compose --env-file .env.production ps
```

Validar salud, dominio y consumidores. No reconstruir las imágenes anteriores
desde código nuevo. Esta reversión de aplicación no revierte cambios de BD.

## Arranque y parada

La política `restart: unless-stopped` reinicia los contenedores cuando vuelve
el daemon, salvo que se hayan detenido explícitamente. El servicio Docker
del sistema debe estar habilitado según su método de instalación.
No es necesario un servicio systemd adicional para Uvicorn.

```bash
docker compose --env-file .env.production stop
docker compose --env-file .env.production start
```

No programar `git pull`/`build`/`up` con cron sin controles: una actualización
debe estar ligada a una versión revisada y verificaciones explícitas.
No ejecutar `docker system prune` ni borrar imágenes de reversión a ciegas.

## Validación local sin BD

Solo cuando el operador lo solicite:

```bash
python -m unittest discover -s deploy/tests -v
docker build -f Dockerfile -t geoportal-api:check .
docker build -f frontend/Dockerfile --target production -t geoportal-web:check .
python deploy/tests/smoke_production.py
```

El smoke utiliza una red Docker interna temporal y API simulada; no publica
puertos ni conecta a PostgreSQL. Comprueba Nginx, vistas, recursos,
redirecciones, rutas/query y errores API JSON. No prueba datos reales,
TLS público ni equivalencia funcional de contratos.

## Aceptación

- Cuatro vistas, navegación, escritorio y móvil.
- Datos de Unidades y Amenazas, filtros territoriales y búsqueda.
- Selección, clustering, detalle, leyendas, mapas base y restablecer filtros.
- Excel, PNG/JPG e impresión; las teselas externas dependen de CORS/red.
- Consultas API de consumidores existentes, propiedades y GeoJSON.
- Certificado válido, CORS, identidad de cliente, rate limit y docs desactivadas.

## Avisos conocidos

El bundle ExcelJS es grande y se descarga al exportar. La revisión anterior
detectó avisos moderados relacionados con `uuid`/ExcelJS; volver a ejecutar
el análisis de dependencias de la versión a publicar. No usar
`npm audit fix --force` sin evaluar incompatibilidades y el bundle precompilado.
