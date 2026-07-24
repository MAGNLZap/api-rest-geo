---
description: Verifica estilo y sintaxis del código
agent: build
---

Verifica que el código esté correcto:

1. Ejecuta imports para detectar errores de sintaxis:
```pwsh
.venv\Scripts\activate; python -c "from app.main import app; print('OK')"
```

2. Ejecuta tests para verificar que todo funciona:
```pwsh
.venv\Scripts\activate; python -m pytest tests/ -v --tb=short
```

Reportar errores encontrados y sugerir correcciones.
