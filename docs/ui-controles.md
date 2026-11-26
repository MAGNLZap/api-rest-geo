# Controles compartidos

La apariencia de campos y selectores Vue se organiza en:

- `frontend/src/styles/institutional-tokens.css`: paleta tomada de la portada,
  compartida por portada, Servicios Sociales y footer institucional.
- `frontend/src/styles/control-tokens.css`: tamaños, radios, espaciado,
  superficies, texto, estados y sombras mediante variables `--ui-*`.
- `frontend/src/styles/selects.css`: campos de selección y menús.
- `frontend/src/styles/text-fields.css`: búsquedas independientes y campos
  con icono, foco en el contenedor y alineación de filtros.
- `frontend/src/styles/interactions.css`: hover, foco y pulsación inspirados
  en la portada. Variables `--ui-interaction-*` controlan contraste, acento,
  sombra y duración; no se redefine toda la paleta de cada página.

Se importan desde `frontend/src/main.ts`. No se modifican los respaldos,
los fallbacks HTML ni la lógica de los filtros.

## Personalización posterior

Cambiar los tokens permite homologar controles sin repetir tamaños o colores
en cada vista. Servicios Sociales usa ahora la paleta de la portada mediante
variables `--brand-*`; `--s-action` referencia el indigo, no un petróleo
independiente. Los mapas anteriores mantienen sus acentos de capa/servicio;
no se reclasificaron sus colores cartográficos.

La paleta corresponde a la identidad implementada en este proyecto, no a
una comprobación externa de un manual oficial de marca:

| Rol | Color |
|---|---|
| Acción, selección y navegación | Indigo `#29265f` |
| Encabezado y footer | Indigo profundo `#201e4c` |
| Acento, borde destacado y ubicación propia | Dorado `#f5c842` |
| Selección suave y avisos informativos | Lavanda `#e9e8f4` |
| Fondos y superficies | `#f4f6fa` y blanco |
| Texto y texto secundario | `#20233a` y `#5e6478` |

El dorado no se utiliza como texto sobre blanco. Gráficos ordinales conservan
etiquetas y cifras además de color; se usan indigo, dorado y dos intensidades
lavanda. Los centros se marcan en indigo; una selección añade dorado y la
ubicación propia es circular con borde indigo.

Navegación: chevrones izquierdo/derecho en lugar de flechas con asta.
Descarga, ubicación y enlace externo conservan sus símbolos funcionales.

No se estilan globalmente todos los inputs: radios, checks y controles
cartográficos mantienen su comportamiento. Los campos con icono se dibujan
como un único contenedor redondeado para evitar doble borde o foco interior
rectangular. En móvil se usa texto de 16px y controles de al menos 46px.

## Menús y compatibilidad

En navegadores con `appearance: base-select`, el desplegable también tiene
radios, sombra, scroll y opciones seleccionadas diferenciadas. En otros se
mantiene el selector nativo del sistema operativo: el campo queda estilizado,
pero no se puede garantizar el mismo aspecto del menú nativo. No se añade
un componente JavaScript que sustituya selección, teclado o eventos.

Validación manual: comprobar escritorio y móvil, opciones largas, teclado,
foco, disabled, lista con scroll, zoom 200% y contraste del sistema.
La revisión de CSS y el build no sustituyen una revisión visual en navegador.

Los hovers con elevación solo se aplican a mouse/puntero fino. Teclado tiene
foco explícito; pantallas táctiles tienen estado de pulsación sin depender
de hover persistente. La preferencia de movimiento reducido elimina
transiciones y elevación. No se cambia padding ni grosor del borde al
hacer hover para evitar saltos de tamaño.

## Orientación y portada

- `home-orientacion.css` adapta los textos de bienvenida del portal público
  de referencia (https://sgde-mtdh.github.io/Geoportal-MTDH/) a las funciones
  existentes. Servicios Sociales es indigo/dorado; el acceso al mapa general
  conserva petróleo y un icono de mapa. No se copian funciones no implementadas.
- `servicios-resultados.css` organiza el progreso centrado y sin caja de
  fondo, fichas de servicio activables, CTA de mapa y botones de cada centro.
- `iconosPublico`, `iconosNecesidad` e `iconosServicio` en `contenido.ts`
  asignan símbolos por identificador sin alterar rutas o recomendaciones.
  `SocialIcon.vue` asigna esos nombres a datos locales de Material Design
  Icons (`@iconify-icons/mdi`, licencia Apache-2.0) y los presenta con
  `@iconify/vue` (MIT). Solo se importan los iconos utilizados; no se carga
  el catálogo completo ni se consulta la API de Iconify en el navegador.
- El tooltip del centro usa tipo de atención, nombre, territorio y distancia
  solo cuando existe referencia. Construye el contenido con nodos de texto,
  sin interpretar HTML de los datos. No contiene botones que desaparezcan
  al retirar el cursor; el punto abre la ficha y sus acciones.

### Progreso del recorrido

Las dos preguntas y los resultados se representan mediante tres hitos
alineados en columnas iguales. La línea une sus centros, detrás de los
círculos, y avanza por tramos completos. El estado actual usa dorado con
anillo exterior; los completados, indigo y check. Los pasos anteriores
son botones para volver y revisar respuestas, con foco visible y acceso por
teclado. Se conservan las selecciones; cambiar de público limpia la necesidad
anterior. El paso actual y los pendientes están deshabilitados: no se permite
saltar preguntas.

El encabezado muestra solo la frase de orientación, inicialmente
«Dos preguntas para orientarte». El conteo de preguntas se conserva
únicamente en el texto accesible del progreso.
Los círculos miden 44px en escritorio y 36px en móvil; los textos
pueden ocupar dos líneas sin reducirse a 10px. Se mantienen `aria-current`,
el valor accesible de progreso, estados completados textuales y el respeto
a movimiento reducido. La consulta directa conserva su tratamiento aparte.

### Tipografía de orientación ciudadana

`orientacion-typography.css` incorpora Changa One en la pregunta
principal de portada, «Elige cómo empezar», la tarjeta de orientación,
las preguntas del recorrido y el título del detalle de servicio.
Se usa su peso original 400, sin negrita sintética ni compresión de letras.
Los subtítulos explicativos del detalle mantienen una familia de lectura.
Una barra dorada corta bajo las preguntas principales aporta un acento
decorativo sin animación; tamaños e interlineado se adaptan a móvil.
No se cambia la tipografía de textos, controles, tarjetas de centros,
KPI ni mapas; conservan sus familias actuales.

La fuente WOFF2 se sirve localmente desde `src/assets/fonts`,
sin solicitudes a Google Fonts en el navegador. El subconjunto latino
incluye tildes, ñ y signos de apertura españoles. Su licencia SIL OFL 1.1
está en `changa-one-OFL.txt`, junto al archivo de fuente.

### Iconografía compartida

Portada, orientación, mapa general y amenazas usan `SocialIcon.vue` para
sus controles. Los iconos decorativos llevan `aria-hidden` y no reciben
foco: el nombre accesible pertenece al enlace o botón. Navegación usa
chevrones; descargas, filtros, cerrar y enlaces externos conservan símbolos
estables entre vistas.

En desarrollo con Docker, `node_modules` usa un volumen propio: instalar
dependencias en Windows no las instala en el servicio `web`. Tras añadirlas,
sincronizar con `docker compose -f compose.dev.yaml exec -T web npm install`
y reiniciar solo `web` si Vite conserva errores de resolución.

Los públicos usan infancia (`human-child`), persona mayor (`human-cane`),
discapacidad (`el:wheelchair`, datos locales de `@iconify-icons/el`),
familia (`human-male-female-child`),
protección (`shield-account-outline`) y otras opciones (`help-circle-outline`).
La silla de ruedas funciona como referencia visual,
no como restricción del público ni de la discapacidad atendida. El encabezado
usa `hand-heart-outline` para expresar acompañamiento.

Iconify permite incorporar otras colecciones, pero cada grupo de controles
debe mantener una familia visual coherente. Se pasan objetos locales al
componente, no nombres que disparen descargas externas. Los SVG de MDI usan
rellenos: no se les aplica el trazo adicional de los antiguos iconos.

Los iconos heredan el contraste del control en hover, foco, pulsación y
selección. Selección y foco destacan con indigo/dorado, sin animaciones
adicionales. Se conserva la respiración del botón de ubicación y su versión
sin movimiento. Las ilustraciones, símbolos de capas, agrupaciones y flecha
de norte cartográfica no se sustituyen por iconos de interfaz.

Revisión visual realizada en Chrome: portada, preguntas y resultados a
390px sin desbordamiento horizontal, y selección/tooltip en escritorio.
No equivale a validación exhaustiva en todos los navegadores.

### KPI y tarjetas de centros

El total se ordena en tres piezas alineadas: icono, cifra y bloque de
etiqueta/territorio. Mantiene el reparto 50/50 con el gráfico en escritorio.
`AnimatedNumber.vue` aplica un efecto decorativo de dígitos durante 480 ms
al montarse o cambiar el valor, sin modificar datos, orden o barras. Cancela
la animación anterior al recalcular; presenta directamente el dato con
movimiento reducido. Lectores de pantalla reciben el número real, no
los dígitos transitorios.

Las tarjetas de centros son compactas, con fondo suave y borde permanente.
El contenedor no tiene hover ni transformación: las acciones pertenecen
a sus botones, que conservan foco, hover y altura mínima de 44px.
