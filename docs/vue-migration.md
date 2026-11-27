# Migración de la presentación a Vue

## Alcance aprobado

FastAPI sigue siendo la API REST geográfica independiente. Vue 3 presenta
la portada y los mapas de Unidades y Amenazas, sin cambiar los contratos
de datos ni añadir funcionalidades nuevas. Leaflet y el diseño se conservan.
Amenazas mantiene su lógica cartográfica conjunta; no se rediseña ni se
divide en nuevas funcionalidades.

## Etapas

- [x] Crear frontend Vue/Vite y acceso configurable a la API.
- [x] Trasladar las tres vistas y conservar controles, capas y exportaciones.
- [x] Preparar desarrollo local y contenedores separados para API y web.
- [x] Documentar despliegue gradual, comprobaciones manuales y reversión.
- [x] Compilar y revisar los cambios; pruebas automatizadas pendientes
      de autorización explícita.

## Decisiones

- Trabajo en el checkout actual por petición del usuario; sin commits.
- Los HTML originales permanecen disponibles y no alimentan el build Vue.
- La navegación entre vistas recarga la página deliberadamente, como antes:
  evita mezclar estilos globales de los dos mapas y conserva los enlaces.
- El código cartográfico imperativo se traslada a controladores por mapa,
  inicializados desde `onMounted`; no se incrusta HTML con `v-html`, iframes
  ni scripts inyectados.
- Las dependencias JavaScript se empaquetan con npm; los recursos
  institucionales existentes se reutilizan mediante alias de Vite.
- No se modifica `.env`, no se migra la BD y no se toca producción.
- No se ejecutan suites automatizadas sin aprobación. La compilación
  y el análisis estático no sustituyen la validación funcional en navegador.

## Verificación de implementación

- Compilación TypeScript/Vue y ambas imágenes Docker: correctas.
- Configuraciones Compose de desarrollo y producción: válidas.
- Configuración Nginx renderizada: sintaxis válida.
- Arranque final de API en Docker con PostgreSQL externo y entorno development.
- Portal local responde HTTP 200 en `http://127.0.0.1:5173/`;
  `/health` de la API informa `healthy` y `database: connected`.
- Análisis Ruff de `app` y `scripts`: correcto.
- No se han ejecutado suites automatizadas ni validación visual en navegador.
- Pendiente de aceptación: comparar mapas/exportaciones con datos reales.
- Riesgo documentado: dependencia moderada de ExcelJS y tamaño de su chunk
  de exportación, que se carga bajo demanda.
- Revisión independiente: sin otras regresiones importantes detectadas.
  Se confirmó que Amenazas requiere PostgreSQL/PostGIS; Docker dev ahora
  utiliza directamente el `.env` existente sin sobrescribir `DATABASE_URL`.

## Ajuste aprobado: desarrollo íntegro en Docker

- Vue y API se ejecutan en `geoportal-mtdh-dev`, con recarga automática.
- Se detuvo el proceso Vue nativo para liberar 5173.
- PostgreSQL/PostGIS externo para ambos mapas: sin fallback SQLite ni
  contenedor/volumen de base de datos en Compose.
- Se retiró `create_all` del lifespan. No se ejecutan migraciones,
  cargas ni creación automática de tablas al iniciar.
- El launcher nativo tampoco sobrescribe ya `DATABASE_URL`.
- Se corrigió el allowlist de Vite para los recursos compartidos fuera
  de `frontend/`, sin permitir todo el repositorio ni sus secretos.
- Se conserva `.env` sin modificaciones.
- `docker compose up -d --build --wait`: API saludable y web iniciado.
- Comprobación HTTP de solo lectura mediante el proxy de Vue: `/health`,
  `/unidades?limit=1` y `/ua_amenazas/data?limit=1` responden 200.
- Recursos compartidos SVG comprobados: respuesta 200.
- Driver del contenedor confirmado: `postgresql+asyncpg`.
- Huella SHA-256 de `.env` idéntica antes y después del ajuste.

## Limpieza conservadora posterior

- Se mantienen los HTML y sus rutas activas como respaldo.
- Se retiraron condiciones duplicadas del router de recursos.
- Se eliminaron constantes, una lectura y una función sin referencias en
  Unidades; Amenazas conserva su lógica y solo pierde un parámetro sin uso.
- Se retiraron `aiosqlite`, las ramas SQLite del cargador y el archivo SQL
  específico de ese motor. No se ejecutó el cargador ni ninguna migración.
- La configuración exige `postgresql+asyncpg`; los errores de validación
  no muestran el valor recibido de la conexión.
- Las fixtures usan PostgreSQL exclusivo con URL explícita, rechazo de
  la BD configurada y esquema aleatorio aislado. No se ejecutaron.
- La BD, `.env` y los contratos de la API permanecen fuera de esta limpieza.
- Se adaptaron los consumidores de las fixtures y se rechazaron parámetros
  que podrían redirigir la conexión de pruebas a otra BD.
- Verificación de limpieza: compilación Vue e imagen API correctas;
  revisión independiente sin hallazgos importantes pendientes. Las
  fixtures PostgreSQL y las suites siguen pendientes de ejecución autorizada.
