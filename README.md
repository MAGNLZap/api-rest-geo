# geoportal-mtdh

Geoportal de consulta territorial y orientación sobre servicios sociales.
Incluye una API GeoJSON con FastAPI y un frontend Vue con mapas Leaflet,
filtros territoriales y exportación de resultados.

## Arquitectura

```text
Navegador → proxy HTTPS propio → geoportal-web (Nginx + Vue)
                                      → geoportal-api (FastAPI)
                                            → PostgreSQL/PostGIS externo
```

- Proyecto Docker Compose: `geoportal-mtdh`.
- Contenedores de producción: `geoportal-web` y `geoportal-api`.
- Una instalación por host con esos nombres fijos; desarrollo usa otro proyecto.
- El código no contiene configuración privada del servidor.
- No se crea una BD, no se ejecutan migraciones ni se cargan datos al arrancar.

## Instalación con Docker

Requiere Docker Engine con Compose v2 o superior, Git y PostgreSQL/PostGIS
accesible con el esquema y los datos preparados. No requiere Python ni Node
en el host; se instalan dentro de las imágenes.

```bash
git clone <URL-DEL-REPOSITORIO> geoportal-mtdh
cd geoportal-mtdh
```

En Linux/macOS:

```bash
install -m 600 deploy/.env.production.example .env.production
```

En PowerShell:

```powershell
Copy-Item deploy/.env.production.example .env.production
```

Completar privadamente `.env.production` con la conexión de BD, orígenes
permitidos y configuración de red. En Windows restringir sus permisos
al usuario/administrador mediante las ACL del sistema.
No usar los valores `CHANGE_ME` ni subir ese archivo a Git.

```bash
docker compose --env-file .env.production config --quiet
docker compose --env-file .env.production build
docker compose --env-file .env.production up -d
docker compose --env-file .env.production ps
```

La web escucha por defecto en `http://127.0.0.1:18081/`.
El proxy público existente debe conservar las rutas y enviar `/` a ese
puerto. TLS, dominio y certificados son responsabilidad de la infraestructura.
Para prueba local sin proxy HTTPS, usar `PUBLIC_SCHEME=http`.

**No aplicar directamente sobre una instalación antigua con otro nombre
de proyecto Compose.** Revisar la transición descrita en la guía antes
de cambiar el tráfico o retirar contenedores.

## Documentación

- [Instalación, configuración y proxy HTTPS](deploy/INSTALL.md).
- [Actualización, reversión y operación](deploy/README.md).
- [Desarrollo y frontend](frontend/README.md).
- [API y preparación de datos](docs/API.md).
- [Seguridad y publicación del repositorio](SECURITY.md).

## Funcionalidades

- Portada y orientación ciudadana: `/` y `/servicios_sociales`.
- Mapa de unidades: `/unidades_infancia`.
- Mapa de amenazas: `/ua_amenazas`.
- API: `/unidades`, `/dpa/*`, `/ua_amenazas/data`, `/health`.
- Reportes Excel e imágenes; los mapas externos requieren conectividad.

## Datos y publicación

Las credenciales, copias de seguridad, bases locales, Excel y CSV operativos
no forman parte de la distribución. Cada instalación debe obtener sus datos
por un canal autorizado. Los límites DPA comprimidos requeridos por la API
se incluyen en `app/data/`; las semillas DPA están en `data/seed/`.

Un `.gitignore` no elimina archivos de commits anteriores. Antes de hacer
público un repositorio existente, revisar también su historial y los derechos
de distribución de datos, imágenes, fuentes y marcas.

## Licencia

El código original y la configuración de despliegue del proyecto se distribuyen
bajo [Apache License 2.0](LICENSE), que permite también uso comercial.
No concede autorización para usar marcas institucionales ni implica respaldo
oficial. Los datasets, logos, imágenes, tipografías y componentes de terceros
no se relicencian por esta declaración: conservan sus derechos y condiciones.
Las licencias de fuentes incluidas se encuentran junto a sus archivos.
