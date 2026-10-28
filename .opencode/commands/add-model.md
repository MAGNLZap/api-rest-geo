---
description: Crea un modelo SQLAlchemy + schema Pydantic
agent: build
---

Crea el modelo solicitado en `$ARGUMENTS`.

1. Inspecciona modelos y migraciones existentes antes de editar.
2. Usa SQLAlchemy 2 (`Mapped`, `mapped_column`) y `__tablename__` explícito.
3. Añade el schema Pydantic solo si una ruta lo necesita.
4. Registra el modelo donde corresponda y crea una migración si afecta una BD persistente.
5. Indica qué validación manual realizar. Ejecuta tests solo si el usuario los aprueba.

No uses `create_all` como sustituto de una migración de producción.
