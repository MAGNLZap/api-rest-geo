# Inclusión y formas de acceso publicadas en Asesor593

Fuentes A0–A5 del [registro](00-fuentes.md). Consulta: **2026-11-24**.
Contenido funcional íntegro en la [captura de ocho fichas](fuentes/asesor593-inclusion-publicada.md).

**Advertencia general:** «publicado» significa que el portal lo devuelve,
no que se haya comprobado su vigencia legal. Los montos, umbrales y
documentos siguientes no son todavía reglas ejecutables de nuestro formulario.

## 1. Cobertura observada

La respuesta de `/api/servicios` contiene 37 registros; 8 tienen
`categoria: "inclusion"` y todos esos 8 tienen `activo: true`.
La categoría se titula **«Inclusión y protección social»**.

El frontend público muestra fichas con información, requisitos, pasos,
canales, modalidad, horario y tiempo estimado cuando está disponible.
Selecciona servicios activos. Los campos API `normativa` y `documentos`
no aparecen como contenido de la plantilla de ficha consultada; se conservan
como metadatos de fuente, no como secciones que hayamos observado renderizadas.

La sección «Otros servicios» devuelve los demás servicios activos, sin
evaluar perfil ni limitarse a la misma categoría. **No es un algoritmo de
orientación individual.** La ficha también publica un aviso general de
gratuidad; no se auditó una tarifa o condición económica por procedimiento.

## 2. Bono Joaquín Gallegos Lara

- **ID:** `bono-joaquin-gallegos`.
- [Ficha pública](https://asesor593.trabajo.gob.ec/servicios/bono-joaquin-gallegos).
- Publica ayuda de **USD 240 mensuales** para personas con discapacidad que
  cumplen condiciones y requieren cuidador.
- Requisitos publicados: porcentaje de discapacidad «establecido» sin
  indicar una cifra; certificación del MSP; Registro Social **2018 ≤
  59.54804 puntos**; inscripción personal.
- Pasos: verificar condiciones; acudir personalmente al Balcón de Servicio
  más cercano; presentar cédula original; realizar inscripción.
- Canales: oficinas MTDH y
  [Contacto Ciudadano Digital](https://www.contactociudadano.gob.ec/).
- Modalidad: mixta. Tiempo: 30 días. Presencial: lunes a viernes,
  08:00–16:45; canal web: 24 horas.

**Pendientes importantes:**

- No completar por suposición el porcentaje de discapacidad.
- No sustituir el umbral 2018 por los de otras fichas o metodologías.
- El metadato `normativa` dice «cédula de identidad y documentos que
  respalden la hoja de vida»: es un contenido aparentemente ajeno al bono,
  no una referencia normativa. No incorporarlo como requisito.
- La ficha no identifica una oficina concreta ni da coordenadas; un CDI
  cercano no equivale a un Balcón de Servicio.
- El texto de inscripción personal no especifica con suficiente precisión
  quién debe comparecer cuando la persona requiere cuidador. No resolver
  esa cuestión por suposición.

## 3. Bono de Desarrollo Humano

- **ID:** `bono-desarrollo-humano`.
- [Ficha pública](https://asesor593.trabajo.gob.ec/servicios/bono-desarrollo-humano).
- Publica transferencia de **USD 55 mensuales** para hogares en pobreza,
  pobreza extrema o vulnerabilidad.
- Requisito en la lista: cédula ecuatoriana o doble nacionalidad.
- Pasos publicados: Registro Social actualizado; extrema pobreza hasta
  **10,52257** y pobreza hasta **29,13091**; condiciones sobre afiliación
  contributiva IESS y servidor público con ingreso mayor a 1 RBU;
  excepciones IESS para Seguro Social Campesino y Trabajo No Remunerado en
  el Hogar; esperar habilitación según presupuesto y prelación; un
  representante de cobro por hogar.
- Modalidad: «En línea». Canal: «Acreditación bancaria», sin enlace de
  solicitud. Publica horarios de canales electrónicos y bancos.

**Interpretación limitada:** no es evidencia de inscripción libre mediante
nuestro formulario. La propia ficha habla de **habilitación**.
No convertir «Acreditación bancaria» en una URL o un trámite inventado.
La referencia normativa exacta está conservada en la captura, sin validación
jurídica realizada aquí.

## 4. BDH componente variable

- **ID:** `bono-desarrollo-humano-variable`.
- [Ficha pública](https://asesor593.trabajo.gob.ec/servicios/bono-desarrollo-humano-variable).
- Publica beneficio para madres con hijos menores de 18 años en pobreza o
  pobreza extrema; `dirigido` y pasos enfatizan extrema pobreza.
- Publica adicionales para menores de 5 años: primer hijo USD 30, segundo
  USD 27, tercero USD 24 y cuarto USD 10; para edades de 5 a menos de 18:
  primero USD 10, segundo USD 9 y tercero USD 8.
- Lista de requisitos: cédula ecuatoriana o doble nacionalidad.
- Pasos: revisar Registro Social; umbrales 10,52257 y 29,13091, atribuidos
  por la ficha a metodología 2025; hijos menores de 18 años; exclusión
  por servidor público del hogar con ingreso superior a 1 RBU; esperar
  habilitación. Publica tercer lugar de prioridad, antes del BDH.
- Modalidad: «En línea». Canal: «Acreditación bancaria», sin enlace.

**Pendientes:** no hay fórmula completa de liquidación, monto base o tope
total explícitos en esta captura. No calcular una prestación sumando
cantidades por cuenta propia. Revisar la diferencia entre la descripción
general de pobreza y la focalización en extrema pobreza.

## 5. Bono 1000 días

- **ID:** `bono-mil-dias`.
- [Ficha pública](https://asesor593.trabajo.gob.ec/servicios/bono-mil-dias).
- Publica acompañamiento económico para gestación y niñas y niños menores
  de 2 años en hogares en pobreza o extrema pobreza.
- Lista de requisitos: constar en Registro Social; situación de pobreza
  o extrema pobreza; gestación o niño/niña menor de 2; condiciones sobre
  afiliación contributiva IESS con las dos excepciones anteriores;
  servidor público del hogar con remuneración mayor a 1 RBU; un
  representante de cobro por núcleo.
- Pasos: revisar Registro Social y puntaje; verificar condiciones;
  cumplir controles de salud para valores condicionados; esperar
  habilitación.
- Modalidad: «En línea». Canal: «Acreditación bancaria», sin enlace.
- El metadato `normativa` cita un decreto de creación con **USD 60**, pero
  la ficha no describe una liquidación completa ni los valores condicionados.

**Pendiente:** no presentar USD 60 como el total de un esquema completo ni
inferir controles, fechas, periodicidades o adicionales no descritos.

## 6. Pensión Mis Mejores Años

- **ID:** `pension-mejores-an`.
- [Ficha pública](https://asesor593.trabajo.gob.ec/servicios/pension-mejores-an).
- Publica **USD 100 mensuales** para personas adultas mayores en pobreza
  o pobreza extrema.
- Lista de requisitos: ser adulto mayor; situación socioeconómica según
  Registro Social; un representante de cobro; condiciones de IESS con las
  excepciones indicadas y de servidor público del hogar.
- Pasos: revisar Registro Social; umbrales atribuidos a metodología 2025;
  esperar habilitación por presupuesto y prioridad; recibir el beneficio.
- Modalidad: «En línea». Canal: «Acreditación bancaria», sin enlace.
- No publica edad numérica en su lista de requisitos. Los 65 años del
  catálogo de atención a mayores del piloto **no son una validación
  independiente de esta pensión**.

## 7. Pensión Toda Una Vida

- **ID:** `pension-toda-una-vida`.
- [Ficha pública](https://asesor593.trabajo.gob.ec/servicios/pension-toda-una-vida).
- Publica **USD 100 mensuales** para personas con discapacidad en pobreza
  o pobreza extrema.
- Lista de requisitos: **menor de 65 años**, discapacidad **≥ 40 %**
  registrada ante MSP, condición socioeconómica según Registro Social y
  condiciones de habilitación.
- Pasos: revisar Registro Social y umbrales atribuidos a 2025; verificar
  discapacidad; esperar habilitación por presupuesto/prioridad; recibir.
- Modalidad: «En línea». Canal: «Acreditación bancaria», sin enlace.

**Límite:** este 40 % no se puede aplicar al BJGL, a atención diurna,
acogida o cuidado comunitario: son servicios distintos.

## 8. Permisos de funcionamiento CDI

- **ID:** `otorgamiento-de-permisos-de-funcionamiento-para-centros-de-desar`.
- [Ficha pública](https://asesor593.trabajo.gob.ec/servicios/otorgamiento-de-permisos-de-funcionamiento-para-centros-de-desar).
- Trámite para brindar atención CDI a niñas y niños de 1 a 3 años.
  Menciona administración directa, convenio, privados y fiscomisionales.
- Público publicado: personas jurídicas públicas/privadas y personas
  naturales ecuatorianas/extranjeras.
- Requisitos publicados: formulario de solicitud; proyecto de funcionamiento
  con enfoque de derechos y articulación; permiso/autorización vigente de
  Bomberos; nómina de usuarios y de talento humano cuando ya funciona;
  plano/croquis georreferenciado; documento del vínculo con el inmueble
  para unidades intramurales.
- Pasos: descargar/llenar formulario y reunir documentos para direcciones
  distritales; visita de inspección coordinada; retirar permiso en dirección
  distrital o coordinación zonal.
- Presencial. Publica horario lunes a viernes 08h00–16h45 y «Puntos de
  atención a nivel nacional», sin dirección concreta.

**Límites:** el primer título de paso y el texto final de normativa están
truncados/contienen erratas. No reconstruir su contenido faltante.
**No son requisitos de matrícula o ingreso infantil.**

## 9. Solicitud de adopción nacional

- **ID:** `solicitud-de-adopcion-nacional-de-ninas-ninos-y-adolescentes-con`.
- [Ficha pública](https://asesor593.trabajo.gob.ec/servicios/solicitud-de-adopcion-nacional-de-ninas-ninos-y-adolescentes-con).
- Solicitud para iniciar adopción nacional de niñas, niños o adolescentes
  con declaratoria de adoptabilidad; evaluación de idoneidad, no
  asignación garantizada.
- Público publicado: persona natural ecuatoriana.
- Lista de documentos publicada: ficha de solicitud; cédula/pasaporte;
  certificado de votación; partida íntegra de nacimiento; documento de
  estado civil; certificado de trabajo e ingresos; antecedentes penales;
  certificado médico general; curso de formación; fotografías del entorno;
  declaración juramentada; autobiografía; carta de aceptación de
  asignación; informe de emparentamiento.
- Publica 11 pasos: contacto con unidad técnica zonal; entrevista inicial;
  formación; presentar solicitud/documentos; evaluación psicosocial;
  visita domiciliaria; declaratoria de idoneidad/no idoneidad; asignación
  cuando corresponda; emparentamiento; fase judicial; seguimiento postadoptivo.
- Presencial. «Oficinas a nivel nacional»; lunes a viernes 08h00–16h45;
  sin coordenadas ni oficina concreta.

**Pendiente:** la lista agrupa documentos que por su nombre se relacionan
con fases posteriores. No exigirlos todos al inicio de nuestro orientador
sin confirmar qué corresponde a cada etapa. La ficha no valida procesos
internacionales, aunque el piloto general los menciona.

## 10. Canales generales, no unidades físicas

A3 publica:

- Portal: https://www.contactociudadano.gob.ec/
- Correo: `informacion@trabajo.gob.ec`.

Son canales generales del portal. No se ha comprobado su tiempo de respuesta,
competencia para cada caso ni relación con una unidad de nuestra BD.

## 11. Uso responsable del complemento

Puede servir para enriquecer las fichas de acceso, mostrando fuente y fecha,
una vez revisado el contenido. No proporciona por sí solo:

- Un motor de elegibilidad ejecutable.
- Una equivalencia completa entre servicios y modalidades de nuestra BD.
- Un inventario geográfico de los canales de acceso.
- Cupos, turnos o capacidad de derivación.
- Autorización para consultar datos personales del usuario.

Los textos «En línea», «Acreditación bancaria» y «24 horas» deben mantenerse
como campos distintos: ninguno demuestra que exista una solicitud digital
o atención humana permanente.
