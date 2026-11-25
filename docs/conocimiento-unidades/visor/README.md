# Visor independiente de revisión

Abrir [`../visor.html`](../visor.html) con doble clic en el explorador.
No necesita Node, Docker, conexión a la app o servidor para utilizarlo.
Los enlaces a fuentes externas solo se abren si los seleccionas.

Desde PowerShell, situado en la raíz del proyecto:

```powershell
Start-Process .\docs\conocimiento-unidades\visor.html
```

## Alcance y diseño

- Diagrama ramificado por público, basado en las 20 rutas capturadas.
- Catálogo de 18 fichas y 8 fichas complementarias de Asesor593.
- Inventario agregado de 4 servicios, 20 modalidades y 22 combinaciones
  observadas en la captura autorizada de PostgreSQL; no consulta la BD al abrirlo.
- Flujo CDI independiente y 14 decisiones pendientes.
- Texto fuente de solo lectura; estado, observaciones y redacción propuesta
  independientes para cada elemento.
- Exportación Markdown/JSON e importación de un borrador de la misma captura.
- Guardado en el navegador cuando permite `localStorage`. Si no lo permite,
  se trabaja en memoria y se muestra una advertencia para exportar.

El estado «Revisado en mesa» no equivale a validación institucional.
No escribir datos personales o información de casos reales en las notas.
El archivo no altera los Markdown originales ni envía las observaciones.
Exportar antes de cerrar es la forma segura de conservar una copia:
el comportamiento del almacenamiento en direcciones `file://` depende
del navegador y las notas no se comparten entre navegadores/computadoras.

Trabajar preferiblemente en una sola pestaña. Si otra ventana cambia el
borrador local, el visor bloquea la sobrescritura y conserva las notas de
esta ventana en memoria. Exportarlas antes de recargar; después se puede
importar ese JSON sobre el borrador recuperado, revisando el aviso de reemplazo.
No es una herramienta de edición colaborativa simultánea.

La interfaz es una mesa de revisión: navegación izquierda, diagrama y
contenido central, observaciones a la derecha. Tipografía del sistema;
azul para evidencia, ámbar para pendientes y verde azulado para acciones.
No reutiliza el diseño gráfico del piloto ni es una propuesta visual
para el geoportal final.

## Archivos y regeneración

- `index.template.html`: estructura accesible y controles.
- `visor.css`: presentación del visor de revisión, adaptable a pantalla pequeña.
- `visor.js`: navegación y borradores locales; no usa APIs.
- `generar.cjs`: incorpora las dos capturas JSON existentes y los recursos
  en un único HTML, sin dependencias npm.
- `../visor.html`: artefacto autónomo para abrir y compartir.

Regenerar desde cualquier directorio:

```powershell
node docs/conocimiento-unidades/visor/generar.cjs
```

Los datos del catálogo y las rutas se leen de los bloques JSON de las
capturas Markdown, no se vuelven a escribir manualmente. No se modifican
esas fuentes. El identificador de captura se deriva de sus contenidos;
un borrador de otra captura se rechaza para evitar mezclar revisiones.

El inventario se lee de `../fuentes/inventario-servicio-modalidad.md`.
Su fecha se registra aparte, también en las notas de sus elementos,
sin invalidar los borradores anteriores de las fuentes públicas. Se avisa
si una nota corresponde a otra fecha de inventario.

`consultar-inventario.py` es una herramienta manual de captura, independiente
del generador y del visor. No se ejecuta al regenerar el HTML. Requiere
autorización explícita para consultar la BD; utiliza la conexión del `.env`
existente sin modificarlo, y transacción de solo lectura. Sobrescribe solo
el Markdown del inventario; archivar la captura previa antes de actualizarla.

## Revisión manual sugerida

- Recorrer los seis públicos y sus veinte rutas.
- Recorrer los cuatro servicios en «Servicios y modalidades»; revisar los
  tres valores de CDI y las etiquetas de mod_abv compartidas entre servicios.
- Comprobar que la ruta «Ver todo el catálogo» no se interpreta como cero servicios.
- Abrir fichas del piloto y los ocho complementos; distinguir equivalencias
  parciales de requisitos de otro trámite.
- Revisar CDI sin simular admisión o selección de centros.
- Escribir notas, cambiar de elemento y volver.
- Exportar Markdown y JSON; importar únicamente el JSON de esta captura.
- Comprobar el aviso de trabajo en memoria si el navegador bloquea el guardado.
- Revisar navegación con teclado y ancho de pantalla pequeño.

No se añaden dependencias al frontend ni rutas a FastAPI. No hay integración
con los contenedores ni cambios en datos de la aplicación.
