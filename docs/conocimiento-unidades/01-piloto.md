# Funcionalidad y contenido del piloto de servicios

Fuentes: P1, P2 y P3 del [registro de fuentes](00-fuentes.md).
La [captura literal](fuentes/piloto-catalogo-y-rutas.md) conserva campos e IDs.

## 1. Cuestionario general: comportamiento observado

P1 usa dos pasos:

1. **«¿Para quién buscas ayuda?»**: seleccionar una opción de `paths`.
2. **«¿Qué necesitas?»**: seleccionar una necesidad de la opción anterior.

Cada paso permite una sola selección. No se puede continuar sin elegir.
Al avanzar del primer paso se limpia la selección de necesidad; al volver
se recupera el público elegido. El resultado muestra la lista de IDs
asociada en el literal `paths`, no una puntuación ni una evaluación normativa.

### Rutas completas

Las etiquetas siguientes omiten únicamente los iconos del piloto.

| Público / ID | Necesidad / ID | Resultado, en el orden definido en P1 |
|---|---|---|
| Una niña o niño / `infancia` | Cuidado y desarrollo infantil / `cuidado` | `cdi`, `cnh` |
| Una niña o niño / `infancia` | Necesita protección / `proteccion` | `proteccion`, `orfandad` |
| Una niña o niño / `infancia` | Quiero conocer otras ayudas / `otra` | `cdi`, `cnh`, `proteccion` |
| Una persona mayor / `mayor` | Cuidado y actividades / `atencion` | `adulto` |
| Una persona mayor / `mayor` | Apoyo económico / `dinero` | `bonos` |
| Una persona mayor / `mayor` | Quiero conocer opciones / `otra` | `adulto`, `bonos` |
| Una persona con discapacidad / `discapacidad` | Atención y acompañamiento / `atencion` | `discapacidad` |
| Una persona con discapacidad / `discapacidad` | Información sobre bonos / `bono` | `bjl`, `bonos` |
| Una persona con discapacidad / `discapacidad` | Otros apoyos / `otra` | `discapacidad`, `sustituto` |
| Mi familia / `familia` | Empezar un negocio / `credito` | `credito`, `emprendimiento` |
| Mi familia / `familia` | Una emergencia o calamidad / `emergencia` | `contingencia` |
| Mi familia / `familia` | Bonos y pensiones / `bonos` | `bonos` |
| Mi familia / `familia` | Apoyo familiar / `otra` | `acompanamiento`, `cnh` |
| Alguien necesita protección / `proteccion` | Se vulneraron sus derechos / `derechos` | `proteccion` |
| Alguien necesita protección / `proteccion` | Bono de orfandad / `orfandad` | `orfandad` |
| Alguien necesita protección / `proteccion` | Necesito orientación / `otra` | `proteccion` |
| Otra ayuda / `otros` | Quiero adoptar / `adopcion` | `adopcion` |
| Otra ayuda / `otros` | Formación para jóvenes / `joven` | `jovenes`, `emprendimiento` |
| Otra ayuda / `otros` | Información o documentos / `tramite` | `ciudadania`, `organizaciones`, `permisos` |
| Otra ayuda / `otros` | Ver todo el catálogo / `otra` | Lista vacía: `showMatches()` abre el catálogo completo |

**Límite:** escoger «Necesita protección» devuelve también `orfandad`
sin preguntar si existe orfandad. Esta es una asociación amplia del piloto,
no evidencia de que ambas situaciones sean equivalentes.

No hay preguntas generales sobre edad, gestación, ingresos, Registro Social,
certificación de discapacidad, documentos o modalidad. Esas condiciones
no participan en el algoritmo de recomendación general.

## 2. Catálogo observado: 18 fichas

Cada ficha contiene `id`, `title`, `short`, `who`, `access`. CDI agrega
`map: true`. El contenido completo de los tres textos está en la captura.

| ID | Nombre publicado | Contenido orientativo distintivo |
|---|---|---|
| `cdi` | Centros de Desarrollo Infantil | Cuidado y desarrollo de niñas y niños de 1 a 3 años; ingreso sujeto a verificación y disponibilidad. |
| `cnh` | Creciendo con Nuestros Hijos | Acompañamiento familiar para gestantes y niñas y niños de 0 a 3 años. |
| `adulto` | Atención a personas adultas mayores | Residencial, diurna, domiciliaria y espacios de encuentro; público de 65 años o más según condiciones. |
| `discapacidad` | Atención a personas con discapacidad | Centros diurnos, acogida inclusiva, hogar y comunidad; criterios de atención y valoración. |
| `proteccion` | Protección especial | Vulneración de derechos; algunos casos requieren derivación o medidas de protección. |
| `adopcion` | Adopciones | Información sobre adopción nacional e internacional; evaluación de idoneidad. |
| `credito` | Crédito de Desarrollo Humano | Financiamiento para emprendimientos; usuarios de determinadas transferencias y condiciones del programa. No aprobación automática. |
| `bonos` | Bonos y pensiones | Transferencias no contributivas; advierte que no todas se solicitan directamente. |
| `contingencia` | Cobertura de contingencias | Calamidades que afectan sustento o vivienda familiar; valoración y normativa. |
| `jovenes` | Atención y formación para jóvenes | Formación y desarrollo para jóvenes de 18 a 29 años según criterios. |
| `emprendimiento` | Formación y apoyo para emprendimientos | Capacidades y vinculación productiva para población objetivo de inclusión económica. |
| `orfandad` | Bono de orfandad | Prestación para niñas, niños y adolescentes en casos previstos; aprobación sujeta a verificación. |
| `sustituto` | Certificación de sustituto por solidaridad humana | Certificación para cuidado de personas con discapacidad; condiciones legales. |
| `bjl` | Bono Joaquín Gallegos Lara | Acceso y acompañamiento técnico según condiciones específicas. |
| `ciudadania` | Atención ciudadana y certificaciones | Información pública y documentos institucionales; canales vigentes. |
| `organizaciones` | Organizaciones sociales | Asesoría, legalización y registro de organizaciones sin fines de lucro. |
| `permisos` | Permisos de funcionamiento | Responsables de unidades sujetas a permisos; trámite y documentación específica. |
| `acompanamiento` | Acompañamiento familiar | Familias usuarias del BDH con componente variable; vinculación por confirmar institucionalmente. |

Los textos de acceso son mayormente genéricos: «consulta», «solicita
orientación», «verificará». No aportan una lista completa de requisitos,
oficinas, responsables o procedimientos para cada modalidad.

El resultado declara:

> Esta orientación es informativa. La institución verifica los requisitos y
> la disponibilidad de atención.

Para las fichas distintas de CDI, P1 muestra:

> El punto de atención para este servicio está pendiente de validación.
> No se muestra un mapa sin ubicaciones verificadas.

## 3. Localizador integrado en el catálogo general

**Observado en `card`, `showLocator`, `updateMap` y `km` de P1:**

- Solo CDI tiene acción de abrir mapa; usa `cdi/centros.json`.
- Filtro por provincia; puede mostrar todo Ecuador.
- Geolocalización voluntaria con radios de **5, 10, 20 o 50 km**; inicial 10 km.
- Autorizar ubicación limpia la provincia seleccionada.
- El filtrado combina provincia y, si hay ubicación, distancia dentro del radio.
- La fórmula calcula distancia geodésica en línea recta; **no calcula rutas,
  tiempo de viaje ni distancia por carretera**.
- El mapa incluye los puntos filtrados con coordenadas numéricas válidas.
- El listado muestra hasta las primeras 100 fichas del orden existente.
  **No hay ordenamiento por cercanía** en ese código.
- Cada resultado ofrece nombre, territorio, dirección y «Cómo llegar» mediante
  enlace de destino a Google Maps.
- «Quitar mi ubicación» elimina `userPos` de la memoria del flujo.
- No solicita cédula ni contiene guardado de ubicación mediante backend,
  cookies o almacenamiento local en este código.
- Esto no implica ausencia de solicitudes de red a proveedores de mapas
  o geolocalización; no se realizó una auditoría de esos proveedores.

P1 advierte que los puntos no representan vacantes disponibles.

## 4. Segundo flujo CDI: independiente

P2 existe en `servicios/cdi/index.html`; el localizador de P1 no navega a
esa página, sino que abre su propia sección inline.

| Pantalla | Dato o acción | Comportamiento observado |
|---|---|---|
| Edad | Menos de 1 año (`under`), 1 año (`1`), 2 años (`2`), 3 años o más (`3`) | Seleccionar habilita seguir. |
| Territorio | Provincia, cantón y parroquia opcional | La provincia habilita buscar; cantón y parroquia filtran en cascada. |
| Resultado | Centros filtrados, mapa, fichas y cómo llegar | Permite nueva búsqueda y acercar el mapa a una ficha. |
| Acceso alternativo | Ver todos los centros | Omite la selección de edad; usa los filtros territoriales que haya en pantalla. |

La función `filtered()` solo revisa provincia, cantón y parroquia.
La edad se usa en `render()` para estos avisos:

- `under`: los centros públicos atienden desde 1 año y para menores se
  requiere orientación sobre otros servicios.
- `3`: atienden principalmente de 1 a 3 años y para 3 años o más se deben
  consultar opciones correspondientes a la edad.

**No hay exclusión por edad ni cambio automático a CNH.** Tampoco se
pregunta fecha de nacimiento, edad en meses, gestación o condiciones familiares.
El límite exacto de «3 años» no se puede decidir a partir de estos avisos.

P2 advierte que el mapa no confirma cupos, horarios actuales o aceptación
de solicitudes, y que no solicita cédulas ni datos personales.

## 5. Datos del piloto: únicamente referencia

P3 contiene **1.849 registros en la captura consultada**, con:

`nombre`, `provincia`, `canton`, `parroquia`, `direccion`, `referencia`,
`administracion`, `lat`, `lon`.

Valores de administración observados:

- `CONVENIO DE COOPERACION`.
- `ADMINISTRACION DIRECTA`.

P2 declara una base georreferenciada de septiembre de 2026. Esa fecha no
demuestra actualización posterior ni debe sustituir el corte de nuestros datos.
No se incorporaron registros del piloto a nuestra BD.

## 6. Ideas funcionales recuperables, no reglas aprobadas

- Partir de lenguaje ciudadano y necesidades, no exigir conocer el nombre
  institucional del servicio.
- Permitir explorar el catálogo sin terminar el cuestionario.
- Explicar público, atención ofrecida y forma de acceso por separado.
- Ofrecer geolocalización voluntaria y alternativa territorial manual.
- Mantener sincronizados filtros, conteo, listado y mapa.
- Distinguir orientación de admisión y mostrar límites de la información.

Son patrones observados. Integrarlos, ampliar las preguntas o cambiar el
ranking será una decisión propia posterior, no una funcionalidad ya existente
ni una regla oficial validada.
