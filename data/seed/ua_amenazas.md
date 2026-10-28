# Dataset UA-Amenazas

`au_amenazadas_data.xlsx` es la fuente principal de atributos e informes. `ua_amenazas_pg.csv` contiene una fila plana por registro y añade del bloque `embedded-ua` únicamente los valores que el HTML necesita para el mapa: coordenadas WGS84, niveles numéricos de amenaza y códigos DPA de filtro.

## Preparación

```pwsh
python scripts/prepare_ua_amenazas_import.py --force
```

El script lee el Excel directamente, lo empareja con `embedded-ua` por `codigo_ua + modalidad` y genera **9869 filas**. No usa un JSON intermediario, no crea catálogos y no conecta ni carga información en PostgreSQL.

## Convenciones

- Una fila por unidad/modalidad/corte. La combinación `fecha_corte + codigo_ua + modalidad` es única.
- El corte del origen es **Septiembre 2026**; `fecha_corte` se representa como `2026-09-01`, convención del primer día del mes.
- Los códigos y nombres originales del Excel se conservan con nombres descriptivos (`provincia_origen`, `codigo_parroquia_origen`, etc.).
- `province_id`, `canton_id` y `parish_id` son códigos de filtro del mapa, como texto; no tienen restricciones FK.
- El código parroquial original del Excel difiere del código usado por el mapa en 3121 filas. Se conservan ambos campos por separado; no se emparejan por nombre.
- `usuarios_hombres`/`usuarios_mujeres` conservan los nulos del informe; `usuarios_hombres_mapa`/`usuarios_mujeres_mapa` conservan los valores usados por el mapa.
- `geom` se exporta como EWKT `SRID=4326;POINT(longitude latitude)`, sin redondeo ni reproyección y con longitud primero. `coordenada_x_utm`/`coordenada_y_utm` permanecen como datos del informe.
- `id`, `created_at` y `updated_at` los genera PostgreSQL.

El DDL provisional está en `scripts/sql/ua_amenazas_provisional.pg.sql` y el diagrama de la tabla plana en `scripts/sql/ua_amenazas.dbml`. Ninguno se ha aplicado a PostgreSQL.

## Importación con Navicat

El CSV tiene una columna `geom` EWKT y coincide con las columnas de datos de la tabla; omite solo `id`, `created_at` y `updated_at`, que tienen valores por defecto en PostgreSQL. En el asistente de Navicat, importa a `ua_amenazas` mapeando las columnas por nombre, deja esos tres campos generados sin mapear y configura campos vacíos como `NULL`. Usa UTF-8.

Haz primero una prueba de importación con una fila y confirma que Navicat convierte `geom` a `geometry(Point,4326)`. El CSV completo contiene 9869 filas.

## Importación alternativa con psql

Desde la raíz del proyecto, con `psql` instalado y conectado a la base correcta:

```pwsh
psql -X -v ON_ERROR_STOP=1 -d geodb -f scripts/sql/import_ua_amenazas.psql
```

El script solo permite cargar cuando `ua_amenazas` está vacía, copia el CSV a una tabla temporal, valida las claves, geometrías y códigos DPA, y luego inserta todo en una transacción. Si falla una validación o un insert, la transacción se revierte. No usar `TRUNCATE` ni ejecutar el script desde otra carpeta: la ruta del CSV es relativa a la raíz del repositorio.
