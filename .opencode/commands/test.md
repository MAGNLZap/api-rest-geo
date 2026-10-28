---
description: Ejecuta la suite de tests
agent: build
---

Ejecuta los tests indicados en `$ARGUMENTS`:

```pwsh
python -m pytest $ARGUMENTS -q
```

Si está vacío, usa `tests/`. Para cambios pequeños, pasar el archivo afectado (ejemplo: `/test tests/test_health.py`).
