# Vista de orientación: uso y revisión manual

## Abrir

Frontend Vue de desarrollo:

- Nueva vista: http://127.0.0.1:5173/servicios_sociales
- Vista original: http://127.0.0.1:5173/unidades_infancia

También hay un acceso «Encuentra apoyo» en la portada Vue. No hay una
nueva ruta HTML en FastAPI: abrir la dirección del frontend, no el puerto
de API. En producción, publicar el build requiere el fallback SPA del
servidor web para esa dirección, igual que las otras rutas Vue. No se
realizó despliegue ni se modificó infraestructura.

## Qué incluye

- Dos preguntas de selección única, las seis opciones de público,
  las veinte rutas y las dieciocho fichas de la captura del piloto.
- Avance directo al elegir una opción, sin confirmación adicional. «Volver»
  permite corregir; se puede volver a elegir la opción anterior.
- Progreso con paso actual, barra y pasos completados. El catálogo abierto
  indica «Consulta directa», sin simular respuestas a las preguntas.
- Fila del servicio activable con clic o teclado para abrir detalles;
  hover y foco diferenciados, sin abrir contenido solo por pasar el cursor.
  CDI destaca «Ver centros en el mapa» como acción independiente y centrada.
- Catálogo abierto, búsqueda por nombre, explicación de resultados y
  fichas con público, descripción y acceso. Sin formulario de elegibilidad.
- CDI: mapa, listado, filtros provincia/cantón/parroquia, búsqueda textual,
  selección sincronizada y resumen territorial del conjunto filtrado.
- Ubicación opcional para ordenar por distancia geodésica. Sin selector
  de radio ni cálculo de rutas/tiempos de viaje. El mapa inicia en los
  doce primeros resultados cuando se usa ubicación; los demás puntos
  permanecen disponibles al explorar el mapa.
- Listado incremental en bloques de doce, con total explícito.
- Google Maps externo para «Cómo llegar», construido con coordenadas.
- Agrupación cartográfica; centros coincidentes accesibles desde un grupo.
- Navegación móvil Lista/Mapa, teclado, diálogo de servicio y mensajes
  accionables de carga/error. No inventa horarios, cupos ni contactos.

## Datos y límites

Los textos se generan desde la captura Markdown:

```powershell
node scripts/generar_catalogo_orientacion.cjs
```

El generador no ejecuta código remoto ni cambia fuentes. El JSON generado
guarda origen, fecha y SHA-256. No integra automáticamente cambios remotos.

La redacción ciudadana se mantiene aparte en
`frontend/src/features/orientacion/redaccion.ts`, aplicada desde `contenido.ts`.
Conserva títulos, IDs y rutas del piloto, y complementa las fichas
correspondientes con Asesor593. Cada detalle muestra sus fuentes y fechas.
Ver [criterios y matriz editorial](08-revision-editorial.md).

El mapa se carga únicamente al solicitar centros, mediante el endpoint
existente `GET /unidades?limit=0&servicio=DESARROLLO+INFANTIL+INTEGRAL`.
La respuesta se reduce en memoria al servicio y modalidad CDI exactos.
Se exige respuesta completa y coordenadas utilizables; no se guarda una
copia de los registros en el frontend. La API actual no permite filtro
`mod`, por lo que devuelve también otras modalidades de desarrollo infantil
que esta vista descarta antes de mostrar. No se modificó el contrato API.

Las otras diecisiete fichas no tienen mapa habilitado en esta primera
versión; no se deduce una homologación por nombre. `mod_abv`, códigos,
datos administrativos y estadísticas de personas no se muestran al usuario.
Los conteos son registros de unidades con coordenadas utilizables, no cupos.
La presencia de coordenadas no acredita una verificación de campo reciente.

La ubicación del usuario se mantiene solo en memoria. No se incorpora a
la consulta API ni a `localStorage`; se elimina con la acción correspondiente,
al reiniciar la orientación o al abandonar la página. Google recibe
peticiones de teselas de la zona visualizada, con idioma español (`hl=es`)
y contexto Ecuador (`gl=EC`), igual que en los mapas existentes.
Google Maps recibe el destino
cuando el usuario abre «Cómo llegar» y maneja su propia política de ubicación.

No se evalúan límites de edad, porcentajes de discapacidad, ingresos o
documentos. Protección/orfandad conserva la asociación original, sin
presentarla como aprobación de un beneficio.

## Revisión manual sugerida

1. Recorrer los seis públicos y sus veinte rutas; confirmar resultados
   y orden frente a `01-piloto.md`. La ruta de catálogo vacío abre las
   dieciocho fichas, no un mensaje de cero resultados.
2. Cambiar público y confirmar que se limpia la necesidad anterior.
   Volver desde resultados y corregir respuestas. Cada elección debe avanzar
   sin «Continuar»; volver a activar la misma opción también debe avanzar.
   Con teclado: Tab recorre opciones sin avanzar, Enter/Espacio selecciona.
3. Abrir/cerrar fichas con teclado, Escape y botón; comprobar el foco.
   Confirmar acceso al catálogo sin responder.
4. Abrir CDI: comprobar que no mezcla CNH u otras modalidades.
   Cambiar provincia/cantón y comprobar limpieza de dependientes.
5. Buscar un centro, limpiar filtros y comprobar que conteo, gráfico,
   listado y puntos corresponden al conjunto filtrado.
6. Seleccionar desde listado y mapa, incluidos centros coincidentes.
   Comprobar resaltado, nombre, dirección y referencia cuando existan.
7. Abrir «Cómo llegar» y contrastar sus coordenadas con el punto elegido.
   Confirmar que avisa del servicio externo.
8. Permitir, denegar y cancelar ubicación. Sin permiso debe poderse buscar
   manualmente. Con permiso, revisar orden, distancias y retirada de ubicación.
9. Simular API inaccesible/timeout y fondo cartográfico inaccesible:
   comprobar reintento y continuidad del listado sin falsos resultados.
10. Revisar a 360 px, con zoom de navegador 200 %, teclado y lector de
    pantalla. Lista/Mapa debe mantener acceso a los controles y detalles.
11. Comprobar que mapa original y vista de amenazas siguen accesibles.

## Verificación técnica

El build incluye comprobación de tipos (`npm run build` en `frontend/`).
No se añaden dependencias ni se ejecutan pruebas automatizadas por defecto.
El build no sustituye esta revisión de interacción y comprensión ciudadana.

Respaldo: [archivos originales y manifiesto](../backups/unidades-original-20261124/README.md).
