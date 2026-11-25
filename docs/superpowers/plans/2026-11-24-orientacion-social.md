# Orientación social Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Crear una vista ciudadana de orientación con formulario y explorador CDI, preservando el mapa existente.

**Architecture:** Vue, datos del piloto generados desde la captura documental,
controlador de búsqueda tipado y componente Leaflet independiente. API sin cambios.

**Tech Stack:** Vue 3, TypeScript, Leaflet y Supercluster existentes.

**Spec:** `docs/conocimiento-unidades/06-diseno-orientacion.md`.

## Global Constraints

- No modificar `.env`, API, BD, Docker ni vista cartográfica original.
- No ejecutar pruebas automatizadas sin petición explícita: validar build,
  tipos, integridad de fuentes y preparar lista de revisión manual.
- Sin dependencias nuevas, commits o despliegues.
- Trabajo en el directorio actual para conservar cambios previos sin
  descartarlos; nuevos archivos y modificaciones puntuales de navegación.

## Review Focus

- Cambios de respuesta o territorio no mantienen selecciones incompatibles.
- Ubicación denegada/tardía no bloquea el formulario ni restaura datos borrados.
- Fallo de API o tiles ofrece recuperación sin fingir resultados completos.
- Conjunto completo en mapa/resumen; listado incremental claramente indicado.
- Google Maps solo recibe coordenadas válidas al abrir el enlace externo.

## Tareas

- [x] 1. Respaldar archivos originales y hashes; generar datos de las 18 fichas
  y 20 rutas desde Markdown con script Node local sin dependencias.
- [x] 2. Crear `frontend/src/features/orientacion/{catalogo.json,contenido.ts,
  useCentros.ts}`: cargar API existente `limit=0`, filtrar CDI exacto,
  validar coordenadas, cascada territorial, orden opcional por distancia,
  búsqueda y selección. No exponer campos técnicos.
- [x] 3. Crear `frontend/src/components/ServiciosMap.vue` y
  `frontend/src/views/ServiciosView.vue`, con CSS separado y SVG original.
  Implementar flujo, estados vacíos/error, accesibilidad, gráfico textual,
  ficha seleccionada y mapa/listado sincronizado.
- [x] 4. Añadir ruta Vue y acceso de portada, conservar acceso anterior.
  Documentar uso, límites y revisión manual; actualizar índice documental.
- [x] 5. Ejecutar build/tipos, comprobar backup e integridad de catálogo;
  revisión estática independiente y corregir hallazgos importantes.

## Registro

No se ejecutarán pruebas automatizadas ni se seguirá el ciclo TDD por la
restricción del repositorio. No se crean worktrees sin autorización;
el respaldo conserva los archivos con cambios previos del usuario.

Build/tipos: `npm run build` completado. Se corrigió el contrato opcional
de props del componente mapa (ausencia como undefined). Advertencia de
chunk grande en ExcelJS existente, no dependencia de la vista nueva.
Hashes de los siete respaldos correctos; cinco archivos de la vista
original sin cambios. App/Home cambian únicamente para ruta y acceso.
Catálogo: seis públicos, veinte rutas y dieciocho fichas idénticos a la
captura, hash fuente conservado. GET del frontend nuevo devuelve HTTP 200.
Revisión visual/interactiva pendiente del usuario.

Revisión estática independiente: se corrigió encuadre de mapa montado en
panel móvil oculto. Espera dimensiones visibles antes de fitBounds y
conserva selección pendiente; segunda revisión no detectó problemas
importantes en esa corrección.

Ajuste solicitado durante la implementación: selección de público/necesidad
avanza inmediatamente, sin botones adicionales. Opciones como botones
nativos, aviso de avance, foco al título y navegación atrás conservada.
Build/tipos volvió a completarse después del ajuste.
