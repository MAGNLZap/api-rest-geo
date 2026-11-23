# Desarrollo, producción y transición desde la instalación actual

## Separación

- FastAPI conserva rutas, contratos, filtros y formatos. No se modifica
  su código para migrar la presentación.
- Vue sirve la portada y los dos mapas.
- Nginx sirve únicamente las tres rutas web y los recursos compilados.
  El resto del espacio `/api-geo/` se envía a FastAPI, incluidos errores.
- La base de datos sigue siendo externa y existente. Esta entrega **no
  migra datos ni instala una nueva BD**.
- Los HTML originales siguen funcionando si se accede directamente a
  FastAPI; permiten conservar la instalación anterior durante la transición.

## Antes de tocar producción

1. Registrar el dominio, puerto real de FastAPI, prefijo publicado,
   proxy/TLS actual, variables y conexión a la BD.
2. Respaldar la BD y la configuración del servicio/proxy según el
   procedimiento de operación existente.
3. Verificar las tres vistas nuevas en un entorno paralelo con datos
   representativos, sin redirigir todavía el tráfico público.
4. Comparar la lista de comprobaciones al final de esta guía.
5. Autorizar el cambio de tráfico de manera separada. Los comandos de
   esta documentación **no se ejecutan automáticamente**.

## Opción A: mantener FastAPI sin Docker y publicar Vue

Esta es la transición de menor impacto para tu instalación actual.
El servicio Python y su conexión a datos permanecen como están.

En una máquina de compilación:

```bash
cd frontend
npm ci
VITE_PUBLIC_BASE=/api-geo/ VITE_API_BASE=/api-geo npm run build
```

En PowerShell, definir primero `$env:VITE_PUBLIC_BASE="/api-geo/"` y
`$env:VITE_API_BASE="/api-geo"` y ejecutar `npm --prefix frontend run build`.

Copiar el contenido de `frontend/dist/` a un directorio versionado en el
servidor, por ejemplo `/srv/apirestgeo/portal/releases/vue-001/`.
No sobrescribir la versión anterior.

La plantilla `deploy/nginx/default.conf.template` también sirve para un
Nginx instalado en el host. Renderizarla con valores explícitos:

```bash
export PUBLIC_PATH=/api-geo
export API_UPSTREAM=127.0.0.1:8001
export WEB_ROOT=/srv/apirestgeo/portal/releases/vue-001
export WEB_LISTEN=127.0.0.1:8080
export PUBLIC_SCHEME=https
export TRUSTED_PROXY_CIDR=127.0.0.1/32

envsubst '${PUBLIC_PATH} ${API_UPSTREAM} ${WEB_ROOT} ${WEB_LISTEN} ${PUBLIC_SCHEME} ${TRUSTED_PROXY_CIDR}' \
  < deploy/nginx/default.conf.template > geoportal-vue.conf
```

Revisar el archivo y colocarlo mediante el procedimiento de administración
de Nginx. El usuario de Nginx necesita lectura sobre `WEB_ROOT`. Esta
configuración escucha en loopback para que el proxy HTTPS actual pueda
enviar `/api-geo/` a `127.0.0.1:8080`, **conservando el prefijo**.

El upstream a FastAPI elimina `/api-geo` exactamente una vez; FastAPI
mantiene `ROOT_PATH=/api-geo`. No añadir una segunda regla que quite ese
prefijo en el proxy de entrada.

Primero validar sintaxis de Nginx y acceder al puerto paralelo. Solo
después cambiar el upstream del proxy público. Ajustar el puerto real de
la API y las redes de confianza a tu infraestructura.

## Opción B: API y web en Docker Compose

Requisitos: Docker Engine/Compose, conectividad del contenedor a la BD
existente y credenciales de ejecución. No copiar la BD a la imagen.

Crear `.env.production` en la raíz tomando
`deploy/.env.production.example` como referencia. **No sobrescribir el
`.env` actual.** Completar la URL de BD y los orígenes externos actuales.

- `localhost` dentro del contenedor no apunta al servidor de BD.
- Para PostgreSQL en otro servidor usar su DNS/IP accesible y permisos
  de red/TLS adecuados a esa instalación.
- `host.docker.internal` puede utilizarse para desarrollo en Docker
  Desktop; en Linux requiere resolver/configurar el host por separado.
- Tanto desarrollo como producción utilizan el PostgreSQL/PostGIS externo
  configurado. No se aprovisiona una BD local ni existe fallback SQLite
  en los arranques de desarrollo.

Validar y construir:

```bash
docker compose --env-file .env.production config --quiet
docker compose --env-file .env.production build
```

No publicar la salida completa de `docker compose config`: puede incluir
las credenciales del entorno.

Después de aprobar la transición, arrancar en paralelo:

```bash
docker compose --env-file .env.production up -d
docker compose --env-file .env.production ps
```

El endpoint de entrada es `http://127.0.0.1:8080/api-geo/`.
La API no publica puerto al host. Se accede a través del proxy:

```text
/api-geo/                       Vue: portada
/api-geo/unidades_infancia      Vue: Unidades
/api-geo/ua_amenazas            Vue: Amenazas
/api-geo/unidades               FastAPI
/api-geo/unidades/raw           FastAPI
/api-geo/unidades/{id}          FastAPI
/api-geo/dpa/*                  FastAPI
/api-geo/ua_amenazas/data        FastAPI
/api-geo/health                 FastAPI + comprobación de BD
```

El proxy público HTTPS existente puede dirigir el espacio `/api-geo/`
a `127.0.0.1:8080`, conservando prefijo, host y el encabezado
`X-Forwarded-For` construido por el propio proxy. No exponer el puerto
8080 directamente a Internet.

`PUBLIC_SCHEME=https` se utiliza detrás de TLS; para una validación local
por HTTP usar `PUBLIC_SCHEME=http`. No confiar en un esquema enviado
arbitrariamente por el cliente.

La red privada `172.30.40.0/24` reserva `.10` para web. FastAPI confía
únicamente en esa IP para encabezados reenviados. Nginx confía en el
gateway `.1` para la IP del cliente reenviada por el proxy del host.
Verificar esta dirección en tu plataforma y ajustar si la topología es
distinta. Si esa subred ya está ocupada, cambiar de forma coordinada
subred, IP de web y ambas listas de confianza antes del arranque.

Comprobar que el rate limit identifica clientes distintos y no agrupa
todo el tráfico en la IP del proxy. Los orígenes CORS de consumidores
externos deben conservarse en `ALLOWED_ORIGINS`.

No hay scripts de carga o migración en el arranque. Se retiró la llamada
preexistente a `create_all`: iniciar o reiniciar la API no modifica el
esquema. Revisar los permisos y el esquema de la BD antes de conectar el nuevo servicio.
La tabla de Amenazas debe existir y contener su dataset, igual que en
la instalación actual.

Para ejecutar solo la API en contenedor puede seguir utilizándose el
`Dockerfile` de la raíz sin compilar Vue ni instalar Node.

## Reversión

- **Solo frontend:** devolver el upstream del proxy a FastAPI/HTML
  anterior o apuntar a la versión estática previamente validada.
- **Docker completo:** devolver el upstream al servicio Python anterior
  antes de detener los contenedores nuevos.
- Conservar el servicio anterior durante la validación. No arrancar
  procesos de carga, limpieza o migraciones durante el cambio.
- No usar `docker compose down -v`: podría eliminar volúmenes de otros
  entornos si se usa el archivo/proyecto equivocado.
- La reversión de presentación no implica restaurar ni borrar datos.

## Comprobaciones manuales de aceptación

### API y rutas

- Consultar los mismos endpoints desde un consumidor externo conocido.
- Comparar estado HTTP, tipo de contenido, propiedades, filtros y
  paginación con la instalación anterior.
- Verificar DPA comprimido, `bbox`, clustering de servidor y errores
  JSON de `/unidades/{id}` y `/dpa/...` inexistentes.
- Verificar que una API desconocida no devuelve el `index.html` de Vue.
- Confirmar que docs no están habilitadas en producción y que CORS,
  rate limit, HTTPS y prefijo continúan funcionando.

### Unidades

- Carga, reintento y estado sin resultados.
- Búsqueda, filtros en cascada, servicio/modalidad y filtros avanzados.
- Resúmenes de unidades/usuarios/urbano-rural.
- Puntos, agrupaciones, hover, selección persistente y Google Maps.
- Provincias/cantones/parroquias, máscara, contorno y modos territoriales.
- Restablecer vista y limpiar filtros; escritorio y pantalla móvil.

### Amenazas

- Todas las amenazas y multiamenaza, regiones y categorías disponibles.
- Filtros territoriales, servicios, modalidad, navegación por territorio.
- UA expuestas/no expuestas, grupos mixtos, códigos y detalle.
- KPI, estadísticas, ranking, leyenda y mapas base.
- Dibujar/quitar polígono y descargar selección.
- Reporte Excel filtrado, hojas, diccionario y banner.
- PNG, JPG e impresión con estadísticas y fuentes.
- Navegar a portada y volver a ambos mapas sin errores.

Las teselas de Google/Esri/OSM y el contorno externo de Ecuador conservan
sus dependencias de red anteriores. La exportación a imagen también
depende del soporte CORS de las teselas. Docker no hace esos servicios
externos disponibles sin conexión.

## Limitaciones conocidas

- La compilación y las imágenes Docker no prueban equivalencia visual o
  funcional: hay que realizar la aceptación anterior con datos reales.
- `npm audit --omit=dev` informa dos entradas moderadas relacionadas
  (`uuid` y su consumidor ExcelJS). ExcelJS utiliza un bundle de navegador
  precompilado: forzar la versión transitiva de `uuid` no garantiza
  reemplazar el código incrustado. No se aplicó `npm audit fix --force`
  porque propone una bajada incompatible de ExcelJS. Evaluar un bundle
  corregido o una sustitución compatible antes de autorizar producción.
- El chunk ExcelJS es grande; se carga solo al exportar, no al abrir el
  mapa. La advertencia de tamaño del compilador queda documentada.
