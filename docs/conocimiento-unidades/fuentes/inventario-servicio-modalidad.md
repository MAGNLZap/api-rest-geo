# Captura agregada: servicio, modalidad y abreviatura

Instante de la transacción: `2026-11-24T17:52:16.877971+00:00`.

Fuente: `unidades_atencion` de la conexión PostgreSQL configurada en el `.env` existente.
No se publican servidor, base, credenciales, nombres de unidades ni datos de personas.

**Transacción confirmada de solo lectura y snapshot REPEATABLE READ.**
Solo se consultaron metadatos de la transacción y la agrupación siguiente.
No se ejecutaron migraciones, cargas o modificaciones.

```sql
SELECT servicio, mod, mod_abv, count(*) AS unidades
FROM unidades_atencion
GROUP BY servicio, mod, mod_abv
ORDER BY servicio NULLS FIRST, mod NULLS FIRST, mod_abv NULLS FIRST
```

Las relaciones son combinaciones observadas, no una taxonomía oficial ni reglas de acceso.
Se preservan los textos exactos, mayúsculas y espacios; NULL y cadena vacía son distintos.
`unidades` cuenta filas de la tabla, no cupos ni códigos institucionales distintos.

| Servicio exacto | Modalidad exacta | Abreviatura exacta | Filas de unidades |
|---|---|---|---:|
| "DESARROLLO INFANTIL INTEGRAL" | "ACOMPAÑAMIENTO FAMILIAR" | "1.- ACOMPAÑAMIENTO FAMILIAR" | 176 |
| "DESARROLLO INFANTIL INTEGRAL" | "CENTROS DE DESARROLLO INFANTIL - CDI" | "1.- EMBLEMATICO" | 75 |
| "DESARROLLO INFANTIL INTEGRAL" | "CENTROS DE DESARROLLO INFANTIL - CDI" | "2.- CDI DIRECTOS" | 51 |
| "DESARROLLO INFANTIL INTEGRAL" | "CENTROS DE DESARROLLO INFANTIL - CDI" | "3.- CDI CONVENIOS" | 1772 |
| "DESARROLLO INFANTIL INTEGRAL" | "CNH altamente dispersa" | "6.- CNH altamente dispersa" | 23 |
| "DESARROLLO INFANTIL INTEGRAL" | "CNH - Misión Ternura" | "4.- CNH - Misión Ternura" | 4389 |
| "PERSONAS ADULTOS MAYORES - PEJ" | "ATENCIÓN DOMICILIARIA" | "3.- DOMICILIAR" | 2042 |
| "PERSONAS ADULTOS MAYORES - PEJ" | "CENTRO GERONTOLÓGICOS DE ATENCIÓN DIURNA" | "1.- DIURNOS" | 71 |
| "PERSONAS ADULTOS MAYORES - PEJ" | "CENTRO GERONTOLÓGICOS RESIDENCIALES" | "2.- RESIDENCIALES" | 56 |
| "PERSONAS ADULTOS MAYORES - PEJ" | "ESPACIOS DE SOCIALIZACIÓN Y ENCUENTRO" | "4.- ACTIVOS" | 268 |
| "PERSONAS CON DISCAPACIDAD" | "ATENCIÓN EN EL HOGAR Y LA COMUNIDAD" | "3.- DOMICILIAR" | 1024 |
| "PERSONAS CON DISCAPACIDAD" | "CENTROS DE REFERENCIA Y ACOGIDA INCLUSIVOS" | "2.- REFERENCIA" | 13 |
| "PERSONAS CON DISCAPACIDAD" | "CENTROS DIURNOS DE DESARROLLO INTEGRAL PARA PERSONAS CON DISCAPACIDAD" | "1.- DIURNOS" | 39 |
| "PROTECCION ESPECIAL" | "ACOGIMIENTO FAMILIAR" | "2.- FAMILIAR" | 3 |
| "PROTECCION ESPECIAL" | "ACOGIMIENTO INSTITUCIONAL" | "1.- INSTITUCIONAL" | 65 |
| "PROTECCION ESPECIAL" | "APOYO FAMILIAR Y CUSTODIA FAMILIAR" | "6.- CUSTODIA" | 65 |
| "PROTECCION ESPECIAL" | "ATENCIÓN Y PROTECCIÓN EMERGENTE - ABRIGO TEMPORAL" | "11.- APE ABRIGO TEMPORAL" | 2 |
| "PROTECCION ESPECIAL" | "ERRADICACIÓN DEL TRABAJO INFANTIL" | "3.- ETI" | 137 |
| "PROTECCION ESPECIAL" | "ERRADICACIÓN PROGRESIVA DE LA MENDICIDAD" | "4.- MENDICIDAD" | 27 |
| "PROTECCION ESPECIAL" | "HABITANTES DE LA CALLE" | "8.- HABITANTES DE LA CALLE" | 3 |
| "PROTECCION ESPECIAL" | "INTERVENCIÓN PSICOSOCIAL PARA LA PREVENCIÓN DE VULNERACIÓNDE DERECHOS DE NNA EN EL ÁMBITOFAMILIAR Y COMUNITARIO–SI" | "9.- INTERVENCIÓN PSICOSOCIAL–SIPS" | 8 |
| "PROTECCION ESPECIAL" | "MOVILIDAD HUMANA - CIUDADES DE ACOGIDA" | "7.- CIUDADES DE ACOGIDA" | 23 |

## Captura estructurada

```json
{
  "format": "ua-service-modality-inventory",
  "version": 1,
  "capturedAt": "2026-11-24T17:52:16.877971+00:00",
  "transactionReadOnly": true,
  "source": {
    "table": "unidades_atencion",
    "query": "SELECT servicio, mod, mod_abv, count(*) AS unidades\nFROM unidades_atencion\nGROUP BY servicio, mod, mod_abv\nORDER BY servicio NULLS FIRST, mod NULLS FIRST, mod_abv NULLS FIRST"
  },
  "totals": {
    "units": 10332,
    "combinations": 22,
    "services": 4,
    "modalities": 20,
    "abbreviations": 20
  },
  "quality": {
    "servicio": 0,
    "mod": 0,
    "mod_abv": 0
  },
  "rows": [
    {
      "servicio": "DESARROLLO INFANTIL INTEGRAL",
      "mod": "ACOMPAÑAMIENTO FAMILIAR",
      "mod_abv": "1.- ACOMPAÑAMIENTO FAMILIAR",
      "unidades": 176
    },
    {
      "servicio": "DESARROLLO INFANTIL INTEGRAL",
      "mod": "CENTROS DE DESARROLLO INFANTIL - CDI",
      "mod_abv": "1.- EMBLEMATICO",
      "unidades": 75
    },
    {
      "servicio": "DESARROLLO INFANTIL INTEGRAL",
      "mod": "CENTROS DE DESARROLLO INFANTIL - CDI",
      "mod_abv": "2.- CDI DIRECTOS",
      "unidades": 51
    },
    {
      "servicio": "DESARROLLO INFANTIL INTEGRAL",
      "mod": "CENTROS DE DESARROLLO INFANTIL - CDI",
      "mod_abv": "3.- CDI CONVENIOS",
      "unidades": 1772
    },
    {
      "servicio": "DESARROLLO INFANTIL INTEGRAL",
      "mod": "CNH altamente dispersa",
      "mod_abv": "6.- CNH altamente dispersa",
      "unidades": 23
    },
    {
      "servicio": "DESARROLLO INFANTIL INTEGRAL",
      "mod": "CNH - Misión Ternura",
      "mod_abv": "4.- CNH - Misión Ternura",
      "unidades": 4389
    },
    {
      "servicio": "PERSONAS ADULTOS MAYORES - PEJ",
      "mod": "ATENCIÓN DOMICILIARIA",
      "mod_abv": "3.- DOMICILIAR",
      "unidades": 2042
    },
    {
      "servicio": "PERSONAS ADULTOS MAYORES - PEJ",
      "mod": "CENTRO GERONTOLÓGICOS DE ATENCIÓN DIURNA",
      "mod_abv": "1.- DIURNOS",
      "unidades": 71
    },
    {
      "servicio": "PERSONAS ADULTOS MAYORES - PEJ",
      "mod": "CENTRO GERONTOLÓGICOS RESIDENCIALES",
      "mod_abv": "2.- RESIDENCIALES",
      "unidades": 56
    },
    {
      "servicio": "PERSONAS ADULTOS MAYORES - PEJ",
      "mod": "ESPACIOS DE SOCIALIZACIÓN Y ENCUENTRO",
      "mod_abv": "4.- ACTIVOS",
      "unidades": 268
    },
    {
      "servicio": "PERSONAS CON DISCAPACIDAD",
      "mod": "ATENCIÓN EN EL HOGAR Y LA COMUNIDAD",
      "mod_abv": "3.- DOMICILIAR",
      "unidades": 1024
    },
    {
      "servicio": "PERSONAS CON DISCAPACIDAD",
      "mod": "CENTROS DE REFERENCIA Y ACOGIDA INCLUSIVOS",
      "mod_abv": "2.- REFERENCIA",
      "unidades": 13
    },
    {
      "servicio": "PERSONAS CON DISCAPACIDAD",
      "mod": "CENTROS DIURNOS DE DESARROLLO INTEGRAL PARA PERSONAS CON DISCAPACIDAD",
      "mod_abv": "1.- DIURNOS",
      "unidades": 39
    },
    {
      "servicio": "PROTECCION ESPECIAL",
      "mod": "ACOGIMIENTO FAMILIAR",
      "mod_abv": "2.- FAMILIAR",
      "unidades": 3
    },
    {
      "servicio": "PROTECCION ESPECIAL",
      "mod": "ACOGIMIENTO INSTITUCIONAL",
      "mod_abv": "1.- INSTITUCIONAL",
      "unidades": 65
    },
    {
      "servicio": "PROTECCION ESPECIAL",
      "mod": "APOYO FAMILIAR Y CUSTODIA FAMILIAR",
      "mod_abv": "6.- CUSTODIA",
      "unidades": 65
    },
    {
      "servicio": "PROTECCION ESPECIAL",
      "mod": "ATENCIÓN Y PROTECCIÓN EMERGENTE - ABRIGO TEMPORAL",
      "mod_abv": "11.- APE ABRIGO TEMPORAL",
      "unidades": 2
    },
    {
      "servicio": "PROTECCION ESPECIAL",
      "mod": "ERRADICACIÓN DEL TRABAJO INFANTIL",
      "mod_abv": "3.- ETI",
      "unidades": 137
    },
    {
      "servicio": "PROTECCION ESPECIAL",
      "mod": "ERRADICACIÓN PROGRESIVA DE LA MENDICIDAD",
      "mod_abv": "4.- MENDICIDAD",
      "unidades": 27
    },
    {
      "servicio": "PROTECCION ESPECIAL",
      "mod": "HABITANTES DE LA CALLE",
      "mod_abv": "8.- HABITANTES DE LA CALLE",
      "unidades": 3
    },
    {
      "servicio": "PROTECCION ESPECIAL",
      "mod": "INTERVENCIÓN PSICOSOCIAL PARA LA PREVENCIÓN DE VULNERACIÓNDE DERECHOS DE NNA EN EL ÁMBITOFAMILIAR Y COMUNITARIO–SI",
      "mod_abv": "9.- INTERVENCIÓN PSICOSOCIAL–SIPS",
      "unidades": 8
    },
    {
      "servicio": "PROTECCION ESPECIAL",
      "mod": "MOVILIDAD HUMANA - CIUDADES DE ACOGIDA",
      "mod_abv": "7.- CIUDADES DE ACOGIDA",
      "unidades": 23
    }
  ]
}
```
