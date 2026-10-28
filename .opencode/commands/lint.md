---
description: Verifica lint y formato de Python
agent: build
---

Ejecuta Ruff sobre `$ARGUMENTS`. Si está vacío, usa `app scripts tests`:

```pwsh
python -m ruff check app scripts tests
python -m ruff format --check app scripts tests
```

No ejecutes tests salvo que el usuario lo pida; `/test` cubre esa tarea.
