# Instalación de geoportal-mtdh

## Requisitos

- Docker Engine y Docker Compose v2 o superior, Git y espacio para imágenes.
- PostgreSQL/PostGIS existente y accesible desde contenedores.
- BD con el esquema y datasets autorizados; consultar [API y datos](../docs/API.md).
- Un proxy público Apache, Nginx o equivalente para HTTPS, dominio y certificados.

En Linux se recomienda Docker Engine instalado mediante el procedimiento
oficial de la distribución. Docker instalado por Snap puede restringir el
acceso a carpetas fuera de `HOME`; no resolverlo haciendo públicos los `.env`.
No instalar dos motores Docker ni desinstalar uno con contenedores activos
sin planificar la migración.

## 1. Obtener y configurar

Clonar en un directorio estable administrado por el operador. No ejecutar
la app desde una carpeta abierta a escritura para todos.

```bash
git clone <URL-DEL-REPOSITORIO> geoportal-mtdh
cd geoportal-mtdh
install -m 600 deploy/.env.production.example .env.production
```

Si `.env.production` ya existe, **no repetir su copia**: editarlo preservando
las credenciales. En PowerShell utilizar `Copy-Item` solo si no existe y
protegerlo con ACL. No compartir la salida completa de `compose config`,
`docker inspect` ni logs sin revisar: pueden incluir información privada.

### Variables de producción

| Variable | Referencia | Uso |
|---|---|---|
| `DATABASE_URL` | obligatoria | `postgresql+asyncpg://usuario:clave@host:5432/base` |
| `ALLOWED_ORIGINS` | orígenes explícitos | Orígenes CORS externos, separados por comas |
| `PUBLIC_SCHEME` | `https` | Esquema público; `http` solo para prueba sin TLS |
| `WEB_PORT` | `18081` | Puerto loopback del host para web |
| `IMAGE_TAG` | obligatorio | Versión inmutable de **ambas** imágenes |
| `GEO_SUBNET` | `172.30.41.0/24` | Subred privada de Compose |
| `WEB_IPV4` | `172.30.41.10` | IP web; es el único proxy confiable para API |
| `GEO_GATEWAY_CIDR` | `172.30.41.1/32` | Gateway confiable del proxy del host |
| `RATE_LIMIT_ENABLED` | `true` | Límite por cliente |
| `RATE_LIMIT` | `120/minute` | Frecuencia admitida |
| `RATE_LIMIT_STORAGE` | `memory://` | Memoria local o Redis externo |
| `LOG_LEVEL` | `INFO` | Verbosidad de logs |

Compose fija producción, `ROOT_PATH` vacío, puerto API interno `8001` y
`ALLOW_LOCAL_NETWORK=false`. No publicar la API directamente al host.
No introducir contraseñas en variables `VITE_*`: terminan en JavaScript público.

En `DATABASE_URL`, `localhost` identificaría el propio contenedor, **no**
el host ni otro servidor. Usar un DNS/IP accesible y configurar los permisos
de PostgreSQL, firewall y TLS correspondientes. Codificar caracteres especiales
de usuario/clave como componentes URL.

Comprobar que la subred no coincide con redes del host, Docker o VPN; una
ruta por defecto no descarta una red remota en uso. Al cambiarla ajustar
también IP web y gateway. Los tres valores de referencia son ejemplos de
infraestructura privada genérica, no direcciones del servidor de producción.

## 2. Construir y arrancar

```bash
docker compose --env-file .env.production config --quiet
docker compose --env-file .env.production build
docker compose --env-file .env.production up -d
docker compose --env-file .env.production ps
```

Usar `sudo docker` si el operador no tiene acceso al daemon. No cambiar el
socket a modo `666`; pertenecer al grupo `docker` equivale a acceso root.

```bash
curl -f --max-time 10 http://127.0.0.1:18081/web-health
curl -f --max-time 10 http://127.0.0.1:18081/health
```

Esperar `200` y `"database":"connected"`; un health correcto no demuestra
que estén todos los datasets ni que los contratos de la API sean equivalentes.
Revisar cuatro vistas, filtros, datos, reportes y clientes externos.

## 3. Proxy HTTPS

La web Docker sirve `/`, las tres vistas y `/assets/`; las demás rutas
se envían a FastAPI, sin prefijo ni fallback HTML para los errores API.
Los recursos compilados usan `/`, por lo que no basta publicar bajo un
subdirectorio: esa variante requeriría cambios coordinados y reconstrucción.

- Apache: [fragmento de referencia](apache/geoportal.conf.example).
- Nginx: [fragmento de referencia](nginx/host.conf.example).

Son fragmentos para el sitio HTTPS existente, **no** configuraciones completas
para copiar sobre otros sitios. Revisar conflictos/orden de reglas, puerto
si se cambió `WEB_PORT`, certificados y renovación. Apache requiere módulos
`proxy`, `proxy_http` y `headers` habilitados.

Respaldar la configuración activa antes de editar. Validar con
`apachectl configtest` o `nginx -t`; recargar solo con sintaxis válida.
Conservar otros sitios y el listener HTTP si se usa para redirección o ACME.
No guardar certificados ni claves TLS en el repositorio ni en las imágenes.

El proxy debe construir `X-Forwarded-For` con una identidad confiable.
Nginx Docker solo confía en `GEO_GATEWAY_CIDR` y FastAPI en `WEB_IPV4`.
Revisar la cadena real si existe balanceador externo, y validar que clientes
distintos no comparten por error el mismo límite de peticiones.
No ampliar las redes de confianza a `*` ni a toda Internet.

Después del cambio comprobar el dominio desde un cliente externo **sin `-k`**,
certificado, navegación, API, CORS y rate limit. Una prueba loopback no valida
DNS, firewall, balanceadores ni TLS público.

## Instalaciones existentes con otro proyecto Compose

Cambiar el campo `name` crea otro proyecto; **no adopta ni renombra**
contenedores existentes. Los nombres nuevos son `geoportal-api` y
`geoportal-web`; no usar `docker rename` como sustituto de actualizar Compose.

Planificar una ventana o un entorno paralelo con puerto, imágenes y subred
distintos, verificarlo y cambiar el proxy solo tras aceptación. Respaldar
configuración, versión de código e imágenes anteriores. No ejecutar
`down`, borrar directorios ni retirar servicios antiguos sin identificar
el proyecto afectado y tener una reversión probada.

Ver [operación y actualizaciones](README.md).
