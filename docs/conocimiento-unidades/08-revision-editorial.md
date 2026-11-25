# Revisión editorial de orientación ciudadana

Revisión de redacción: **25/11/2026**. Fuentes capturadas: **24/11/2026**.

## Alcance aprobado

Mejorar los textos en toda la experiencia conservando la intención y las
definiciones del piloto y Asesor593, sin copia literal obligatoria.
No cambiar las dos preguntas, las seis opciones de público, las veinte
asociaciones ni el orden de sus resultados. No modificar reglas de acceso,
datos, mapas o elegibilidad.

## Separación entre evidencia y redacción

- `frontend/src/features/orientacion/catalogo.json` conserva la captura
  literal generada del piloto; no contiene las adaptaciones editoriales.
- `frontend/src/features/orientacion/redaccion.ts` reúne resumen, definición,
  público, acceso, aclaraciones y complementos de los 18 servicios.
- `contenido.ts` aplica esa redacción manteniendo IDs, títulos, orden y
  disponibilidad del mapa originales, y construye referencias por ficha.
- `scripts/generar_catalogo_orientacion.cjs` sigue generando solo la captura
  original. Regenerar no borra las adaptaciones.
- Las capturas Markdown de ambas fuentes y el visor documental no se
  reescriben: siguen permitiendo comparar el original con la adaptación.

Cada ficha pública permite abrir sus fuentes. La fecha de redacción no es
una nueva consulta de fuentes ni una validación de vigencia jurídica.

## Criterios editoriales

1. Preservar la finalidad del servicio y el nombre del catálogo.
2. Distinguir qué ofrece, a quién se dirige y cómo acceder.
3. Evitar descripciones tan genéricas que oculten si se trata de cuidado,
   acompañamiento, una transferencia, financiamiento o un trámite.
4. Complementar con Asesor593 solo en correspondencias documentadas.
5. No equiparar prestaciones por compartir público o palabras.
6. No reconstruir requisitos incompletos ni convertir metadatos erróneos
   en instrucciones para la ciudadanía.
7. Los montos publicados se identifican con la fecha de captura; no se
   calculan pagos ni se promete habilitación.

## Matriz de las 18 fichas

P = [captura del piloto](fuentes/piloto-catalogo-y-rutas.md).
A = [captura de Asesor593](fuentes/asesor593-inclusion-publicada.md).

| ID del piloto | Base | Tratamiento editorial |
|---|---|---|
| `cdi` | P | Cuidado/desarrollo, edades publicadas, consulta de ingreso y disponibilidad. Permiso de funcionamiento no se trata como ingreso familiar. |
| `cnh` | P | Gestación y familias con niñas/niños de 0–3; acompañamiento, no bono. |
| `adulto` | P | Conservar cuatro modalidades y 65 años o más como información, sin evaluación automática. No equiparar con una pensión. |
| `discapacidad` | P | Conservar centros diurnos, acogida, hogar/comunidad; no trasladar condiciones de transferencias. |
| `proteccion` | P | Vulneración de derechos y posible derivación/medidas. Conservar asociación original con orfandad, explicando que no acredita el beneficio. |
| `adopcion` | P + A adopción nacional | Mantener alcance nacional/internacional del piloto, limitar el complemento de etapas/documentos a nacional. Solicitud no garantiza asignación. |
| `credito` | P | Financiamiento para personas usuarias de determinadas transferencias; no aprobación automática ni equivalencia con formación. |
| `bonos` | P + A seis prestaciones | Distinguir BDH, BDHV, 1000 días, Mis Mejores Años, Toda Una Vida y BJGL. Informar sobre habilitación, no inventar inscripción digital. |
| `contingencia` | P | Calamidades que afectan sustento/vivienda; verificación del caso. Sin añadir subsidios o canales. |
| `jovenes` | P | Atención/formación, 18–29 publicados y convocatorias; sin inventar programas abiertos. |
| `emprendimiento` | P | Capacidades y vinculación productiva; distinguir de crédito. |
| `orfandad` | P | Prestación para los casos previstos; consulta de solicitud/documentos sin inventar condiciones. No adopción. |
| `sustituto` | P | Certificación relacionada con cuidado, no bono o pensión. |
| `bjl` | P + A BJGL | Explicar ayuda económica y cuidado; preservar acceso publicado y advertir porcentaje no precisado y comparecencia por confirmar. |
| `ciudadania` | P | Información pública y certificaciones de documentos institucionales; no ampliar a cualquier trámite ciudadano. |
| `organizaciones` | P | Asesoría/legalización/registro de organizaciones sociales sin fines de lucro; no organizaciones laborales por semejanza. |
| `permisos` | P + A permiso CDI | Responsables de operar unidades. Complemento CDI específico, no requisitos universales ni matrícula familiar. |
| `acompanamiento` | P | Familias usuarias del BDH variable; acompañamiento distinto de transferencia y vinculación por confirmar. |

Los seis complementos de `bonos`, más adopción y permisos, cubren las ocho
fichas de inclusión capturadas. BJGL también tiene su ficha propia.

## Información que no se reconstruye

- Porcentaje de discapacidad de BJGL.
- Fórmula completa, base y tope del BDHV.
- Esquema completo de valores condicionados de 1000 días.
- Textos truncados del permiso y metadatos erróneos de normativa.
- Documentos de adopción exigibles en cada etapa.
- Extremo de edades CDI/CNH en meses y su uso como filtro.
- Cupos, contactos, oficinas concretas o horarios de cada centro.

Para Toda Una Vida se conserva como **información de su propia ficha** el
umbral publicado de discapacidad y edad; no se aplica a otros servicios
ni se pregunta para excluir a usuarios del formulario.

## Textos de interfaz

Se revisan portada, introducciones, ayudas bajo los públicos, resultados,
detalle y fuentes. Se evita «disponible» cuando podría interpretarse como
cupo confirmado. Las denominaciones y opciones de las dos preguntas
permanecen iguales al piloto.

## Comprobación

- [x] Contraste de las 18 redacciones con el catálogo y el cruce documental.
- [x] Referencias de complementos contrastadas con las ocho fichas capturadas.
- [x] Integridad de IDs/rutas/fuentes y build de Vue.
- [x] Revisión estática independiente de fidelidad y límites.

Comprobación: 18 adaptaciones completas; las ocho fichas de Asesor593
referenciadas existen en la captura. Catálogo literal, hash de fuente
y rutas originales conservados. La revisión independiente señaló que
debía conservarse el acompañamiento técnico del BJGL mencionado por el
piloto; se incorporó a la definición junto a la ayuda económica.

No se ejecutan pruebas automatizadas, consultas de BD, migraciones,
despliegues ni cambios de `.env`.
