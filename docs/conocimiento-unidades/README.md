# Base de conocimiento para la orientación de Unidades de Atención

**Fecha de consulta:** 24 de noviembre de 2026.

**Estado:** investigación de fuentes públicas, no reglas de negocio aprobadas
ni implementación de un formulario.

## Alcance acordado

Extraer contenido y funcionamiento de los servicios sociales del piloto
Geoportal-MTDH y complementarlo con Asesor593 para preparar nuestra propia
orientación ciudadana, conectada después a nuestras unidades actualizadas.

Quedan fuera:

- El Niño, ENOS, amenazas y sus funcionalidades.
- Colores, componentes gráficos, estilos, convenciones visuales y maquetación.
- Importar la base de centros del piloto a nuestra aplicación.
- Modificar la API, formularios, `.env`, bases de datos o despliegues.
- Inventar requisitos, montos, contactos, disponibilidad o decisiones de acceso.

## Cómo leer la evidencia

| Etiqueta | Significado |
|---|---|
| **Observado en código** | Comportamiento explícito del piloto o del JavaScript público consultado. No equivale a una norma institucional. |
| **Observado en datos** | Combinación exacta presente en la captura agregada autorizada de la BD. No implica pertenencia normativa, elegibilidad o cupos. |
| **Publicado en ficha/API** | Texto que la fuente publica. No implica que hayamos verificado su vigencia jurídica. |
| **Correspondencia candidata** | Relación de significado para revisión; todavía no es un enlace automático entre servicios. |
| **Propuesta** | Organización de la información o mejora funcional nuestra; no se atribuye a las fuentes. |
| **Pendiente** | Información ausente, contradictoria o insuficiente para tomar una decisión. |

Las capturas literales conservan cifras y erratas de las fuentes para poder
auditarlas. **No deben convertirse automáticamente en validaciones del futuro
formulario.** Un resultado orientativo no determina elegibilidad, inscripción,
asignación de cupo o aprobación de un beneficio.

## Documentos

**Revisión visual:** abre [el visor HTML independiente](visor.html) con doble
clic para recorrer diagramas, consultar fichas y exportar observaciones.
No requiere servidor ni se conecta a la app. [Instrucciones del visor](visor/README.md).

1. [Fuentes y método de consulta](00-fuentes.md).
2. [Cuestionarios, catálogo y localización del piloto](01-piloto.md).
3. [Contenido de inclusión y acceso de Asesor593](02-asesor593.md).
4. [Cruce entre fuentes, datos propios y decisiones pendientes](03-cruce-y-pendientes.md).
5. [Captura literal del catálogo y rutas del piloto](fuentes/piloto-catalogo-y-rutas.md).
6. [Captura literal de las ocho fichas de inclusión de Asesor593](fuentes/asesor593-inclusion-publicada.md).
7. [Pertenencia observada entre servicios y modalidades](04-servicios-modalidades.md).
8. [Captura agregada de servicio, modalidad y abreviatura](fuentes/inventario-servicio-modalidad.md).
9. [Criterios acordados para evolucionar el formulario y propuestas UX](05-criterios-formulario.md).
10. [Diseño de la nueva orientación y criterios de usabilidad](06-diseno-orientacion.md).
11. [Acceso, límites y revisión manual de la vista Vue](07-uso-orientacion.md).
12. [Revisión editorial: intención, definiciones y trazabilidad de las 18 fichas](08-revision-editorial.md).

## Alcance actual del formulario

Se acuerda conservar un alto grado de equivalencia funcional con el piloto,
anotando diferencias sustentadas y mejoras de experiencia de usuario.
No se incorpora por ahora selección de múltiples necesidades ni apoyos
complementarios personalizados. Las preguntas y respuestas son el mecanismo
para orientar entre modalidades; cualquier distinción nueva requiere
documentar su criterio, no inferirlo de la proximidad o del nombre.
Ver [decisiones, observaciones y propuestas](05-criterios-formulario.md).

## Hallazgos principales

- La consulta agregada posterior y autorizada de la BD encontró **4 servicios,
  20 modalidades y 22 combinaciones**, con **10.332 filas de unidades**.
  `mod_abv` no es una clave única y CDI tiene tres valores para una modalidad.
  Ver [análisis y límites](04-servicios-modalidades.md). La investigación
  inicial de fuentes públicas no había consultado datos de la BD.

- El piloto general contiene **18 fichas**, **6 tipos de público** y **20
  asociaciones público/necesidad**. Sus dos preguntas son «¿Para quién buscas
  ayuda?» y «¿Qué necesitas?».
- No evalúa edad, Registro Social, discapacidad certificada o documentación
  para resolver esas asociaciones: devuelve listas fijas de servicios.
- Solo la ficha CDI habilita el mapa del catálogo general.
- Existe un **segundo flujo CDI separado**, con edad y territorio. No debe
  confundirse con el cuestionario general ni presentarse como si ambos ya
  estuvieran integrados.
- La edad en ese flujo CDI cambia avisos, **no filtra centros ni admite/rechaza
  solicitudes**.
- Asesor593 respondió con 37 servicios en total; la categoría pública
  `inclusion` contiene **8 fichas activas en esta captura**. No es una
  correspondencia uno a uno con las 18 fichas generales del piloto.
- La ficha de **permiso de funcionamiento CDI es para la autorización de una
  unidad**, no para que una familia ingrese a su niña o niño a un CDI.
- El piloto no demuestra cupos; Asesor593 no aporta coordenadas de oficinas
  concretas en las fichas de inclusión capturadas.
- Hay datos incompletos e inconsistencias que requieren revisión institucional,
  especialmente límites de edad CDI, contenido del BJGL y montos/condiciones de
  transferencias. Están señalados en los documentos, no resueltos por suposición.

## Regla de uso para el siguiente trabajo

La mejora puede reorganizar preguntas y redacción, pero debe mantener separadas:

1. La necesidad expresada por la persona.
2. El servicio que podría orientarla.
3. La modalidad de atención y sus unidades geográficas.
4. Los requisitos y canales publicados para acceder.
5. La verificación institucional que no podemos sustituir.

Esta separación es una **propuesta de organización**, no una regla jurídica
extraída de las fuentes. Antes de programar el cuestionario se deben resolver
las preguntas de [validación](03-cruce-y-pendientes.md#5-decisiones-que-requieren-validación).
