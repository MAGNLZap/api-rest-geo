---
description: Crea un modelo SQLAlchemy + schema Pydantic
agent: build
---

Crea un nuevo modelo para el proyecto.

Uso: `/add-model <Nombre> [campos]`

Ejemplo: `/add-model Place name:str description:optional longitude:float latitude:float category:optional`

## Pasos

1. Crear modelo en `app/models/<nombre_lowercase>.py`:
   - Heredar de `Base` (app/models/base.py)
   - Usar `Mapped` y `mapped_column` de SQLAlchemy
   - `id` como primary key autoincremental
   - `longitude: Mapped[float]` y `latitude: Mapped[float]`
   - Otros campos según los proporcionados

2. Importar el modelo en `app/main.py` (para que `create_all` lo registre)

3. Crear schema Pydantic en `app/schemas/<nombre_lowercase>.py` (si es necesario)

## Convenciones

- `__tablename__` en snake_case plural (ej: `geo_places`)
- Usar `String(255)` para strings, `Text` para descripciones largas
- `Float` para coordenadas
- `nullable=True` para campos opcionales
