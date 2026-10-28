---
description: Crea un endpoint GeoJSON siguiendo los patrones actuales
agent: build
---

Crea el endpoint solicitado en `$ARGUMENTS`.

1. Carga el skill `geo-endpoint`.
2. Inspecciona primero el router, modelo y schema más cercanos.
3. Implementa el cambio mínimo con SQLAlchemy async y `Depends(get_db)`.
4. Registra routers nuevos en `app/main.py`.
5. Indica qué validación manual realizar. Ejecuta tests solo si el usuario los aprueba.

No inventes módulos compartidos ni uses `app/schemas/geo.py`: no existe en este proyecto.
