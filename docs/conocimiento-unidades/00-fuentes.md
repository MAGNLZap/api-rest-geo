# Fuentes, trazabilidad y límites

Consulta realizada el **2026-11-24** mediante lectura de HTML, JavaScript
público y respuestas GET públicas. No se ejecutó JavaScript remoto para extraer
las reglas; los literales del piloto se analizaron estáticamente.

## 1. Piloto Geoportal-MTDH

- Repositorio: https://github.com/sgde-mtdh/Geoportal-MTDH
- Commit consultado: `36eec6664f38af0eb1dcd3c1f17aa79c65480468`.
- Fecha del commit según GitHub: `2026-11-18T20:48:13Z`.
- Árbol asociado al commit: `252496c0cfd846016f728f0a1c8b91e985447486`.

| ID | Fuente | Uso en esta investigación |
|---|---|---|
| P0 | [Portada publicada](https://sgde-mtdh.github.io/Geoportal-MTDH/index.html) | Identificar el acceso a servicios; no estudiar ENOS. |
| P1 | [Servicios publicados](https://sgde-mtdh.github.io/Geoportal-MTDH/servicios/index.html) / [código fijado](https://github.com/sgde-mtdh/Geoportal-MTDH/blob/36eec6664f38af0eb1dcd3c1f17aa79c65480468/servicios/index.html) | Literales `services`, `paths`; funciones de orientación y mapa. |
| P2 | [CDI publicado](https://sgde-mtdh.github.io/Geoportal-MTDH/servicios/cdi/index.html) / [código fijado](https://github.com/sgde-mtdh/Geoportal-MTDH/blob/36eec6664f38af0eb1dcd3c1f17aa79c65480468/servicios/cdi/index.html) | Flujo CDI independiente; edad, territorio y resultados. |
| P3 | [Base CDI fijada](https://github.com/sgde-mtdh/Geoportal-MTDH/blob/36eec6664f38af0eb1dcd3c1f17aa79c65480468/servicios/cdi/centros.json) | Solo estructura, número de registros y administraciones; no importación. |

La respuesta de P1 publicada y el archivo `servicios/index.html` del commit
consultado fueron **idénticos byte a byte** en esta consulta.

P1 declara que su información resumida proviene de la matriz de taxonomía
MIES de abril de 2025. **No se encontró esa matriz original entre los archivos
del repositorio consultado**: no se ha comprobado que el resumen reproduzca
toda la matriz ni su normativa.

## 2. Asesor593

| ID | Fuente | Uso |
|---|---|---|
| A0 | https://asesor593.trabajo.gob.ec/ | Entrada pública al portal. |
| A1 | https://asesor593.trabajo.gob.ec/api/categorias | Identificar `inclusion`: «Inclusión y protección social». |
| A2 | https://asesor593.trabajo.gob.ec/api/servicios | Leer contenido completo recibido y seleccionar `categoria === "inclusion"`. |
| A3 | https://asesor593.trabajo.gob.ec/api/contacto/canales | Canales generales publicados; no oficinas georreferenciadas. |
| A4 | https://asesor593.trabajo.gob.ec/main-EWLG5UZY.js | Confirmar qué GET públicos alimentan catálogo y fichas. |
| A5 | https://asesor593.trabajo.gob.ec/chunk-Cbe23CQz.js | Confirmar uso de `activo`, requisitos, pasos, canales y datos adicionales en la ficha. |

El HTML inicial de Asesor593 contiene una aplicación dinámica; la extracción
de texto estático por sí sola no muestra el catálogo. Se consultaron los GET
que el propio frontend público utiliza. No se usó autenticación, no se
accedió a administración ni se enviaron formularios, solicitudes o valoraciones.

Los bundles con nombre hash identifican lo observado en esta visita; pueden
cambiar o dejar de estar disponibles en otro despliegue. Los hashes SHA-256
de las respuestas fuente están en las capturas Markdown.

Las ocho fichas son **el resultado observado en A2**, no una afirmación de que
ese sea el inventario completo y definitivo de todos los servicios sociales
de la institución.

## 3. Proyecto propio

- [Modelo de unidades](../../app/models/unidad_atencion.py).
- [Propiedades expuestas por la API](../../app/schemas/unidad_atencion.py).
- [Vista actual](../../frontend/src/views/UnidadesView.vue).
- [Controlador actual](../../frontend/src/features/unidades/map.js).

Se revisó código local para distinguir variables disponibles de reglas que
todavía no existen. **No se consultó la BD externa ni se compararon inventarios
reales de servicios/modalidades.** La vigencia y mayor amplitud de nuestros
datos son contexto indicado por el usuario, no una auditoría realizada aquí.

## 4. Límites de la verificación

- No se verificó jurídicamente ninguna norma o resolución citada por Asesor593.
- No se comprobó disponibilidad real de cupos, contactos, horarios o pagos.
- No se realizó una prueba interactiva completa en navegador.
- Se excluyeron las funcionalidades y contenido de ENOS; no se incorporó su
  información de contingencias o respuesta.
- No se adoptaron estilos, imágenes, iconos ni convenciones gráficas.
- No se ha decidido un esquema de elegibilidad, un formulario nuevo ni una
  integración automática entre ambos sistemas.

Las mejoras y correspondencias propuestas se identifican como tales.
