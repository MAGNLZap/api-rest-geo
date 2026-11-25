# Respaldo previo a la vista de orientación

Capturado el 24/11/2026 antes de añadir `/servicios_sociales`.
`manifest.json` registra los SHA-256 de los archivos originales, incluidos
sus cambios locales previos. Se conserva la estructura relativa del proyecto.

- `UnidadesView.vue`, controlador `map.js`, `unidades.css` y fallback HTML:
  no se modificaron para el rediseño.
- `leaflet.js`: dependencia compartida preservada, sin cambios.
- `App.vue` y `HomeView.vue`: estado previo a añadir ruta y acceso.

Es una copia de los archivos relevantes de la vista, no un respaldo de BD,
dependencias o todo el repositorio. No contiene `.env` ni credenciales.
La vista original continúa en `/unidades_infancia`; no hay que restaurar
archivos para usarla. No sobrescribir esta copia al actualizar la nueva vista.
