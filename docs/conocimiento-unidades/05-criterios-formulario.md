# Criterios acordados para evolucionar el formulario

Actualización: 24/11/2026. Este documento registra el alcance acordado y
organiza observaciones y mejoras propuestas. No implementa el formulario
ni modifica las capturas originales.

## 1. Decisión de alcance

**Acordado con el usuario:**

- Partir del formulario del piloto con un grado alto de equivalencia
  funcional, en lugar de diseñar otro cuestionario desde cero.
- Mantener como referencia sus preguntas, selecciones, rutas y resultados.
  Cualquier diferencia debe justificarse con una observación sustentada
  en lo recabado o una mejora de experiencia de usuario.
- No incorporar por ahora la propuesta de múltiples necesidades o de
  apoyos complementarios personalizados. Una selección puede seguir
  mostrando varios resultados, como ya ocurre en el piloto.
- Utilizar las respuestas a preguntas como mecanismo para orientar entre
  servicios o modalidades. No sustituirlo por la elección automática del
  centro más cercano ni por coincidencias de nombres.
- Mantener separadas orientación y aprobación institucional de acceso.

La equivalencia es funcional y de contenido, **no una copia del diseño
gráfico**. Se mantiene el alcance independiente de ENOS y amenazas.

## 2. Línea base que se conserva

| Componente | Comportamiento de referencia | Fuente |
|---|---|---|
| Público | «¿Para quién buscas ayuda?», seis opciones, selección única | P1, `paths` |
| Necesidad | «¿Qué necesitas?», opciones dependientes del público, selección única | P1, 20 asociaciones |
| Resultado | Fichas asociadas a la ruta elegida, conservando inicialmente su orden | P1, `showMatches()` |
| Catálogo | «Ver todo el catálogo» abre las 18 fichas, no un resultado vacío | P1 |
| CDI separado | Edad, territorio y resultados; no confundirlo con el cuestionario general | P2 |

Detalle y fuentes: [comportamiento del piloto](01-piloto.md) y
[captura literal de rutas](fuentes/piloto-catalogo-y-rutas.md).

La línea base sirve para comparar: no convierte sus asociaciones amplias
en reglas aprobadas ni obliga a reproducir problemas detectados.

## 3. Preguntas para orientar modalidades

**Objetivo acordado:** que las respuestas permitan orientar una modalidad
frente a otra cuando esa distinción sea necesaria.

**Límite observado:** el cuestionario general actual solo pregunta público
y necesidad. No diferencia todas las modalidades de nuestra BD. La página
CDI pregunta edad, pero esa respuesta solo cambia avisos; no filtra centros.

Por tanto:

1. Conservar las preguntas existentes como punto de partida.
2. Identificar qué rutas ya orientan suficientemente y cuáles dejan varias
   modalidades sin distinguir.
3. Para cada distinción necesaria, documentar la pregunta candidata,
   opciones, respuesta que activa cada resultado y fuente del criterio.
4. Si falta evidencia para la condición, registrar «pendiente de validar»;
   no inventar umbrales ni presentar una decisión automática como vigente.
5. Enlazar el resultado con las unidades de la combinación servicio/modalidad
   homologada. Territorio y distancia sirven para localizar después, no
   para determinar la modalidad adecuada por sí solos.

No se acuerda añadir de inmediato preguntas a todas las rutas. Primero se
revisa si las existentes bastan. Las nuevas preguntas o cambios de lógica
deben quedar explícitos como diferencias respecto del piloto.

## 4. Observaciones y mejoras de experiencia de usuario

Las siguientes son propuestas concretas para revisar, no cambios ya
implementados ni nuevas condiciones de acceso:

| Elemento existente | Observación sustentada | Mejora propuesta | Efecto sobre la lógica |
|---|---|---|---|
| Dos pasos generales | El resultado depende de público y necesidad | Mostrar progreso, respuesta seleccionada y acción clara para volver y corregir | Ninguna nueva condición |
| Cambio de público | La necesidad depende del público y se limpia al avanzar en P1 | Si cambia el público, limpiar necesidad y resultados incompatibles, indicando que se debe elegir de nuevo | Evitar resultados de una rama anterior |
| Resultados fijos | No explican una evaluación individual | Mostrar «Estas opciones aparecen porque elegiste…» con las respuestas y fuente | Explica la asociación, no prueba elegibilidad |
| «Necesita protección» | Devuelve protección y orfandad sin preguntar por orfandad | Señalar la asociación para revisión; evaluar si basta aclarar el resultado o hace falta una pregunta específica | Cualquier cambio de asociación queda pendiente, no se corrige por inferencia |
| Edad CDI | Cambia avisos, no centros; el extremo de 3 años es ambiguo | Explicar el alcance del aviso y registrar la validación del límite antes de convertirlo en filtro | No añadir exclusiones no verificadas |
| Fichas de servicio y acceso | Permiso de funcionamiento CDI corresponde a operadores, no a ingreso familiar | Diferenciar claramente destinatario y finalidad en el texto y las acciones | Evita mezclar trámites sin crear requisitos |
| Modalidades propias | `mod_abv` se repite entre servicios y CDI tiene tres valores | Mostrar nombres comprensibles; conservar servicio y modalidad completa para identificar la relación | No enlazar solo por abreviatura |
| Localización | Cercanía no acredita cupos ni competencia; P1 no ordena por proximidad | Distinguir «Ver unidades» de «Cómo acceder» y declarar qué orden y distancia se muestran | No usar distancia como regla de admisión |
| Geolocalización y catálogo | Existe consulta manual y catálogo abierto | Mantener alternativas sin permiso de ubicación, etiquetas claras, foco visible y controles utilizables con teclado | No exigir datos personales adicionales |

Fuentes de las observaciones:
[piloto](01-piloto.md), [Asesor593](02-asesor593.md),
[cruce y pendientes](03-cruce-y-pendientes.md) e
[inventario propio](04-servicios-modalidades.md).

## 5. Relación entre los tres conjuntos de información

| Conjunto | Función en esta fase | Lo que no se debe asumir |
|---|---|---|
| Piloto: 18 fichas y 20 rutas | Línea base del formulario | Que cada ficha sea un servicio de BD o una única modalidad |
| BD: 4 servicios, 20 modalidades y 22 combinaciones | Evidencia de las combinaciones que pueden localizarse después de homologar | Que los conteos permitan elegir modalidad o acrediten cupos |
| Asesor593: 8 fichas de inclusión | Complementar descripción, acceso y observaciones | Que «Presencial/En línea» equivalga a la modalidad de atención |

La matriz de homologación deberá registrar, por cada ruta: ficha del piloto,
servicio y modalidad exactos de BD si corresponden, complemento de Asesor593,
tipo de relación, fuente y estado de validación. **Una correspondencia
candidata no habilita por sí sola una regla del fcuestionario.**

## 6. Registro de cada diferencia

Para revisar el formulario sin rediseñarlo implícitamente, cada cambio
debe documentar:

- Pregunta o ruta original y resultado actual.
- Observación y evidencia, con fecha.
- Cambio propuesto: redacción, interacción, pregunta o asociación.
- Resultado esperado y si altera la lógica.
- Estado: observado, inferido, propuesto, acordado en alcance o pendiente
  de validación institucional.

El acuerdo de alcance no aprueba por sí solo cada texto, pregunta o regla.
No se han modificado la app, las rutas originales ni las capturas fuente.
