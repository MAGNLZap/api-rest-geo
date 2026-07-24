---
description: Ejecuta la suite de tests
agent: build
---

Ejecuta los tests del proyecto:

```pwsh
.venv\Scripts\activate; python -m pytest tests/ -v $ARGUMENTS
```

Si `$ARGUMENTS` está vacío, ejecuta todos los tests. Si contiene un filtro, pasar como argumento a pytest (ej: `/test test_health`).
