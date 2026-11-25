# Pertenencia observada entre servicios y modalidades

## Evidencia y alcance

El 24/11/2026 se consultaron exclusivamente `servicio`, `mod`, `mod_abv`
y `count(*)` de `unidades_atencion`, en una transacción PostgreSQL confirmada
de solo lectura, con aislamiento REPEATABLE READ.
[Consulta, instante exacto y captura](fuentes/inventario-servicio-modalidad.md).

No se modificaron registros ni esquema, no se ejecutaron migraciones o cargas
y no se publican datos de conexión, nombres de unidades o personas.
El visor incorpora esta captura; abrirlo **no consulta la BD**.

## Resumen del inventario

| Servicio exacto | Modalidades distintas | Combinaciones exactas | Filas de unidades |
|---|---:|---:|---:|
| DESARROLLO INFANTIL INTEGRAL | 4 | 6 | 6.486 |
| PERSONAS ADULTOS MAYORES - PEJ | 4 | 4 | 2.437 |
| PERSONAS CON DISCAPACIDAD | 3 | 3 | 1.076 |
| PROTECCION ESPECIAL | 9 | 9 | 333 |
| **Total** | **20** | **22** | **10.332** |

No se observaron valores NULL, vacíos o compuestos solo por espacios en estos
tres campos. Cada valor exacto de `mod` aparece bajo un solo servicio en
esta captura. Esto describe los registros existentes, no garantiza una
restricción formal o una clasificación inmutable.

Los conteos representan filas, no cupos, capacidad, personas atendidas,
ubicaciones distintas ni códigos institucionales distintos.

## Cómo leer la relación

```text
servicio observado
  └── modalidad exacta (mod)
        └── valor de mod_abv + cantidad de filas con esa combinación
```

En el visor, «Servicios y modalidades» permite seleccionar cada servicio,
modalidad o combinación y dejar una revisión separada.

### mod_abv no es una clave única

Dos etiquetas aparecen en más de un servicio:

- `1.- DIURNOS`: mayores y discapacidad, con modalidades completas distintas.
- `3.- DOMICILIAR`: mayores y discapacidad, también con modalidades distintas.

Además, la modalidad `CENTROS DE DESARROLLO INFANTIL - CDI` presenta:

| Valor exacto de mod_abv | Filas |
|---|---:|
| 1.- EMBLEMATICO | 75 |
| 2.- CDI DIRECTOS | 51 |
| 3.- CDI CONVENIOS | 1.772 |
| **Total de esa modalidad** | **1.898** |

Por tanto, no asumir que `mod_abv` es siempre una abreviatura literal.
Estas diferencias requieren un diccionario institucional antes de llamarlas
submodalidades, administración o criterios de acceso.

## Qué queda pendiente

- Homologar las 18 fichas del piloto con estas cuatro denominaciones de
  servicio y sus modalidades. Son niveles de agrupación diferentes, no
  catálogos intercambiables.
- Validar condiciones que orientan de una necesidad a una modalidad.
  La pertenencia observada no demuestra elegibilidad.
- Confirmar significado y estabilidad de `mod_abv`, y decidir los
  identificadores del catálogo futuro.
- Mantener separados los canales de Asesor593 («Presencial», «En línea»)
  de la modalidad de atención de una unidad.

**Propuesta para una futura integración:** obtener las modalidades disponibles
del conjunto de unidades del servicio seleccionado, sin unir servicios por
etiquetas compartidas de `mod_abv`. No se han cambiado los filtros de la app.

## Borradores del visor

La incorporación del inventario conserva el identificador de las dos capturas
públicas originales, para poder recuperar los borradores previos. Las notas
nuevas de inventario registran además el instante de su evidencia. Si una
captura futura cambia ese instante, se avisa al abrir una nota antigua.
Las claves de servicio/modalidad/combinación se basan en sus textos exactos,
no en el orden de los registros. Un borrador con elementos ya inexistentes
se rechaza, en lugar de perder notas silenciosamente.
