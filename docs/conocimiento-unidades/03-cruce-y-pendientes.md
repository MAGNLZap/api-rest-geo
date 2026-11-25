# Cruce de conocimiento y límites para el futuro formulario

Este documento **no define reglas aprobadas ni implementa funcionalidades**.
Relaciona lo observado y señala lo que falta antes de diseñar nuestra solución.
Fuentes: [registro](00-fuentes.md), [piloto](01-piloto.md) y [Asesor593](02-asesor593.md).

## 1. Correspondencias candidatas

La coincidencia de palabras no basta para enlazar servicios. Cada fila
requiere validar finalidad, público, modalidad y canal de acceso.

| Servicio del piloto | Complemento encontrado en las 8 fichas de Asesor593 | Alcance y límite |
|---|---|---|
| `cdi` | Ficha de permiso CDI | **No equivalente:** autorización para operar una unidad, no ingreso de una familia. No completar la ficha de acceso familiar con esos requisitos. |
| `cnh` | Bono 1000 días menciona gestación y menores de 2 años | **No equivalente:** un beneficio monetario no sustituye acompañamiento familiar. No se encontró una ficha CNH en la captura. |
| `adulto` | Pensión Mis Mejores Años | Complemento económico posible, no equivalencia con atención residencial/diurna/domiciliaria. |
| `discapacidad` | Pensión Toda Una Vida y BJGL | Complementos económicos posibles, no equivalencia con centros diurnos, acogida u hogar/comunidad. |
| `proteccion` | Sin ficha específica en la captura | No usar adopción u orfandad como sustitutos generales de protección especial. |
| `adopcion` | Solicitud de adopción nacional | Correspondencia parcial: el piloto incluye nacional e internacional; la ficha consultada solo acredita contenido para nacional. |
| `credito` | Sin ficha específica en la captura | No confundir financiamiento con BDH o BDHV. |
| `bonos` | BDH, BDHV, Bono 1000 días y las dos pensiones; BJGL también tiene ficha propia | Grupo amplio frente a prestaciones distintas. Su eventual desglose es una propuesta de organización que necesita validación. |
| `contingencia` | Sin ficha específica en la captura | No incorporar reglas de ENOS; tampoco inventar un canal o subsidio. |
| `jovenes` | Sin ficha específica de inclusión en la captura | Los servicios de empleo del portal se excluyeron de esta investigación. |
| `emprendimiento` | Sin ficha específica de inclusión en la captura | No sustituirlo por capacitación laboral por semejanza de nombre. |
| `orfandad` | Sin ficha específica en la captura | No equiparar a adopción. |
| `sustituto` | Sin ficha específica en la captura | No convertirlo en un requisito del BJGL o en una pensión. |
| `bjl` | Bono Joaquín Gallegos Lara | Coincidencia de denominación y finalidad. Falta validar requisitos vigentes e inconsistencias del contenido publicado. |
| `ciudadania` | Canales generales del portal | Complemento de contacto, no ficha completa de certificaciones/información pública. |
| `organizaciones` | Sin ficha específica de inclusión en la captura | No homologar automáticamente con organizaciones laborales de otra categoría. |
| `permisos` | Permisos de funcionamiento CDI | Correspondencia parcial: esa ficha no cubre permisos de todas las unidades/modalidades. |
| `acompanamiento` | La ficha BDHV describe una transferencia del público mencionado por el piloto | Relación contextual, no equivalencia entre acompañamiento y transferencia. |

«Sin ficha» significa **no encontrada en el conjunto consultado**, no
inexistencia del servicio en la institución.

## 2. Qué aportan nuestros datos, según el código revisado

Se revisaron modelo y esquemas locales, no valores reales de la BD.

**Actualización posterior:** se autorizó y realizó una consulta agregada
de solo lectura de `servicio`, `mod` y `mod_abv`. El inventario y sus límites
están en [Servicios y modalidades](04-servicios-modalidades.md). Esa captura
no homologa los IDs del piloto ni resuelve requisitos de acceso.

| Necesidad de información | Campos disponibles | Lo que no se puede inferir |
|---|---|---|
| Identificar una unidad | `id`, `co_siimdh`, `nombre` | Unicidad institucional y persistencia del código entre cortes requieren comprobarse. |
| Relacionar atención y modalidad | `servicio`, `mod`, `mod_abv`, `tipo` | Los IDs del piloto no están homologados con los valores de estos campos. |
| Localizar territorialmente | `dpa_prov`, `dpa_can`, `dpa_par` y sus nombres; `region`, `area` | Competencia territorial para recibir una solicitud o cobertura efectiva de un servicio. |
| Situar y describir una ubicación | Coordenadas GeoJSON; `longitude`, `latitude` en salida raw; `dir`, `ref`, `link_ubi` | Distancia por carretera, accesibilidad, transporte o tiempo real de llegada. |
| Administración y organización | `tipo_admin`, `cooperante`, `uni_des`, `dis_sen`, `zon_plan`, `ruc` | Que cualquier unidad de esa administración pueda realizar cualquier trámite. |
| Resúmenes de atención | `hombre`, `mujer`, `total`, `asis_prom`, `asistencia` | Cupos libres, capacidad máxima, demanda futura o admisión de una persona concreta. |
| Información social por registro de unidad | `rs18`, `no_rs18`, `ext_pob18`, `pob18`, `no_pob18` y equivalentes `25` | Puntaje individual del visitante ni validación de su condición. Confirmar definiciones antes de construir KPI. |
| Contexto temporal/textual | `corte` | Su significado, formato y correspondencia exacta con el periodo deben confirmarse; no asumirlo por el nombre. |

En este modelo no hay campos explícitos de:

- Vacantes, turnos, horarios de cada unidad o contactos telefónicos.
- Requisitos de acceso por modalidad y su vigencia.
- Protocolo de recepción de derivaciones.
- Solicitudes, expediente, persona derivada, estado o responsable del caso.
- Verificación individual de Registro Social, discapacidad o documentos.

No se debe completar ninguna de esas ausencias con valores supuestos del piloto.

## 3. Separaciones propuestas para organizar el conocimiento

**Propuesta nuestra, pendiente de aprobación:**

1. **Necesidad ciudadana:** lo que expresa la persona.
2. **Servicio informativo:** finalidad, público, condiciones publicadas y fuente.
3. **Modalidad de atención:** qué tipo de intervención se presta.
4. **Unidad geográfica:** dónde se presta esa modalidad según nuestra base.
5. **Canal del trámite:** dónde se orienta, verifica, solicita o recibe.
6. **Decisión institucional:** evaluación que el orientador no puede aprobar.

Ejemplos sustentados en las fuentes:

- Familia que busca cuidado infantil y responsable que solicita permiso CDI
  son usuarios y procedimientos distintos.
- Centro cercano y oficina habilitada para tramitar un bono no son
  intercambiables.
- Cobrar por acreditación bancaria no demuestra un mecanismo de solicitud
  digital.
- Ser población destinataria potencial no confirma requisitos ni cupo.

Estos ejemplos explican por qué no debe existir un `match` basado solo en
coincidencia textual entre nombres de servicios.

## 4. Inventario de preguntas ya sustentadas en las fuentes

No es todavía un formulario nuevo; indica qué variables aparecen realmente.

| Tema | Evidencia disponible | Límite para usarlo |
|---|---|---|
| Para quién se busca ayuda | 6 opciones de P1 | No cubre explícitamente todos los públicos del catálogo; por ejemplo, CNH menciona gestantes sin una opción inicial específica. |
| Necesidad | 20 asociaciones en P1 | Asociaciones amplias; no equivalen a comprobaciones de condiciones. |
| Edad infantil | Opciones de P2; edades en CDI, CNH y Bono 1000 días | No resolver límites de edad ambiguos ni compartir un mismo intervalo entre servicios distintos. |
| Edad de personas mayores | 65 o más en la ficha general de atención del piloto | No extrapolar automáticamente a toda transferencia económica. |
| Juventud | 18–29 en texto del piloto | No existe pregunta numérica ni validación normativa en su algoritmo. |
| Gestación | Texto CNH y Bono 1000 días | Condiciones de ambos servicios son distintas. |
| Discapacidad y apoyo/cuidado | Texto del piloto y fichas BJGL/Toda Una Vida | El 40 % está publicado para Toda Una Vida, no para todos los servicios. |
| Situación social | Varias fichas de transferencias de A2 | No tenemos verificación individual ni una metodología única compartida entre todas las fichas. |
| Territorio | Provincia/cantón/parroquia en P2; provincia en P1 | Domicilio o cercanía no demuestra jurisdicción competente. |
| Ubicación voluntaria y radio | P1: 5, 10, 20 y 50 km | Distancia geodésica, no tiempo de traslado; alternativa manual disponible. |
| Persona que busca un trámite institucional | Adopción, permisos, organizaciones, certificaciones | No mezclar requisitos del operador de unidad con los de sus usuarios. |

Una pregunta adicional, un orden nuevo, reglas de descarte o una puntuación
serían decisiones nuevas. No se incluyen como hechos en esta base.

## 5. Decisiones que requieren validación

### Antes de diseñar las rutas

1. ¿Qué servicios y modalidades exactos existen actualmente en nuestra BD?
   El [inventario autorizado](04-servicios-modalidades.md) ya captura los
   valores reales y sus conteos. Sigue pendiente homologarlos con el piloto
   y validar identificadores y significado institucional de `mod_abv`.
2. ¿Qué parte de los 18 grupos del piloto pertenece al alcance del mapa de
   unidades y qué parte solo tendrá orientación o enlace externo?
3. ¿Qué distingue cada modalidad de un mismo servicio y qué variables
   permiten orientarla sin realizar una valoración profesional?
4. ¿Cuáles son los límites de edad oficiales, especialmente CDI/CNH, y
   cómo deben expresarse: años, meses, inclusión/exclusión de los extremos?
5. ¿Cuáles son los requisitos vigentes de acceso familiar a CDI? La ficha
   de permisos de Asesor593 no los proporciona.

### Antes de publicar información sensible para decisiones

6. Validar montos, puntajes, metodología de Registro Social y condiciones
   de transferencias, sin trasladar requisitos de una prestación a otra.
7. Corregir/confirmar el texto ajeno en `normativa` del BJGL y el porcentaje
   de discapacidad no especificado.
8. Confirmar fórmula del BDHV, valores condicionados de 1000 días y
   diferencias de focalización en las fichas.
9. Confirmar documentos de adopción según fase y completar textos truncados
   de permisos sin reconstruirlos por inferencia.
10. Identificar oficinas/canales competentes, contactos y horarios verificables.

### Antes de llamar al resultado «derivación»

11. Definir si el producto solo orienta y ubica, o registra/envía una
    derivación formal. Las fuentes revisadas no prueban integración de casos.
12. Determinar quién recibe, acepta y sigue una derivación y si existe
    información real de capacidad/cupos. Hoy no está acreditada.
13. Definir atención de situaciones urgentes y vulneración de derechos con
    protocolo institucional; no inventar canales de emergencia ni reglas
    de priorización.
14. Acordar si se conserva alguna respuesta o ubicación y con qué propósito,
    consentimiento y plazo. Los pilotos no justifican recoger cédulas.

## 6. Qué sí podemos mejorar sin inventar conocimiento

**Criterio de alcance posterior:** preservar la equivalencia funcional con
el formulario del piloto y justificar diferencias mediante observaciones
y mejoras UX. No incorporar múltiples necesidades por ahora.
Las preguntas orientarán entre modalidades cuando los criterios estén
documentados. Ver [acuerdo y propuestas concretas](05-criterios-formulario.md).

**Propuestas, no reglas ya aprobadas:**

- Unificar redacción y separar familias, personas cuidadoras, solicitantes
  de adopción y responsables de unidades cuando el trámite lo requiera.
- Explicar por qué una opción informativa aparece, citando la respuesta
  y la fuente correspondiente.
- Mostrar «requisitos por confirmar» cuando la fuente sea incompleta,
  en lugar de aprobar/rechazar personas.
- Separar «Ver unidades que prestan atención» de «Cómo acceder al trámite».
- Usar nuestra base geográfica, no los puntos históricos del piloto.
- Si se decide ordenar por distancia, implementar y declarar el cálculo
  real: el piloto solo filtra por radio y no ordena por cercanía.
- Mantener consultas manuales y catálogo abierto para no obligar a revelar
  ubicación o completar un perfil.
- Mostrar fuente y fecha de revisión de cada condición.

La siguiente fase debe convertir únicamente el conocimiento validado en
preguntas, condiciones y enlaces a unidades. Esta investigación no cambia
ni la API ni el mapa de Amenazas.
