# Diseño acordado: orientación de servicios sociales

## Objetivo y alcance

Una entrada práctica, sencilla y legible para personas que buscan ayuda
social, incluidas personas en situación de vulnerabilidad. Mantener las
dos preguntas del piloto, selección única y las 18 fichas. No añadir
preguntas de elegibilidad ni descartar personas por edad, documentación
o situación social. Las asociaciones originales se conservan.

La interfaz no muestra `mod_abv`, códigos, indicadores de personas atendidas,
ni campos administrativos. No es una evaluación de acceso.

## Experiencia

Formulario → opciones de servicio → detalle y siguiente acción.
Cada opción de público o necesidad avanza directamente al activarla, sin
botones «Continuar» o «Ver opciones». Se anuncia este comportamiento antes
de las opciones. Botones nativos permiten explorar con Tab y elegir con
Enter/Espacio; el foco pasa al título del siguiente paso. «Volver» conserva
las respuestas y permite activar la misma opción de nuevo. Cambiar de
público limpia la necesidad incompatible.
Solo CDI tiene enlace cartográfico homologado inicialmente: servicio exacto
`DESARROLLO INFANTIL INTEGRAL`, modalidad exacta
`CENTROS DE DESARROLLO INFANTIL - CDI`. Las demás fichas siguen disponibles
con orientación y enlace institucional. No habilitar otros mapas solo por
coincidencias textuales o existencia de registros.

Mapa y listado sincronizados. Provincia, cantón y parroquia encadenados;
ubicación opcional, sin selector de radio. Con ubicación, orden geodésico
ascendente declarado; sin ubicación, orden alfabético dentro del territorio.
No llamar cercanos a resultados sin referencia. Las filas de resultados
representan unidades, no cupos. Listado paginado visualmente con «Ver más»;
el resumen y los puntos se refieren al conjunto filtrado, no a la página.

Ficha: nombre, tipo de atención en lenguaje sencillo, territorio, dirección
y referencia si existen. Cómo llegar abre Google Maps con coordenadas
validadas; no ejecutar `link_ubi` arbitrario. No inventar horarios, teléfonos,
fotos de centros, disponibilidad o tiempos de viaje.

La ubicación precisa solo se usa en memoria para ordenar; no se almacena ni
se envía a nuestra API. Google Maps y proveedor cartográfico son externos.
Denegación/ausencia de ubicación conserva búsqueda manual.

## Diseño visual

Inspiración funcional: exploración de resultados, filtros y mapa/listado
de plataformas como Airbnb, no copia de marca ni funcionalidades comerciales.

- Base blanca `#ffffff`, fondo azul hielo `#f2f6fa`, texto índigo `#172b46`,
  acción petróleo `#12666b`, acento azul `#3159b8`, líneas `#d7e1eb`.
- Montserrat local para títulos, sistema para texto y controles.
- Formulario central con opciones amplias; resultados en filas editoriales
  y mapa protagonista, no un tablero de tarjetas idénticas.
- Escritorio: listado y mapa contiguos. Móvil: selector Lista/Mapa.
- Resumen propio y compacto: total filtrado y distribución territorial
  de centros. Gráfico con equivalente textual, sin datos sensibles.
- Foco visible, contraste, teclado, errores accionables, movimiento reducido.
- Un SVG abstracto original como recurso decorativo; no aparentar fotografías
  verificadas de centros.

## Preservación y acceso

Crear `/servicios_sociales` en Vue sin modificar la ruta ni los archivos de
la vista original `/unidades_infancia`. Añadir un acceso desde la portada.
Respaldar vista, controlador, CSS, dependencia Leaflet compartida y fallback
HTML existentes con hashes, antes de los cambios. No tocar `.env`, API,
BD, Docker, amenazas ni desplegar.

## Actualización de conocimiento

`mod_abv` es información interna. La utilidad para el ciudadano prima sobre
exponer todos los campos de BD. Asesor593 sirve como complemento en
construcción, no como árbitro de contradicciones. La asociación protección/
orfandad se conserva como orientación original, no como diagnóstico.

Consulta oficial del 24/11/2026:

- https://www.desarrollohumano.gob.ec/desarrollo-infantil-integral/
  Publica CDI 1–3 años, CNH gestantes/0–3 y acompañamiento para BDHV;
  describe administración directa/emblemáticos y convenios. No resuelve
  el extremo de edad en meses ni la separación local emblemático/directo.
- https://www.desarrollohumano.gob.ec/atencion-a-personas-adultas-mayores/
  Describe residencial, diurna, espacios de encuentro y domiciliaria.
- https://www.desarrollohumano.gob.ec/servicios-mies-para-personas-con-discapacidad/
  Describe las tres modalidades observadas y distingue acceso de prestación.
- https://www.desarrollohumano.gob.ec/servicios-de-proteccion-especial/
  Permite contrastar varias modalidades, no una homologación completa.

Estas páginas son evidencia publicada, no validación normativa exhaustiva.
El prototipo usa la captura del piloto como texto de referencia y señala
su carácter orientativo.
