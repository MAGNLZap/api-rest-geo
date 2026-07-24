---
description: Inicia el servidor de desarrollo
agent: build
---

Inicia el servidor de desarrollo FastAPI:

```pwsh
.venv\Scripts\activate; python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

Si el puerto 8001 está ocupado, usar el siguiente puerto disponible (8002, 8003, etc.).

El servidor se inicia en modo recarga automática (--reload). Swagger disponible en http://localhost:8001/docs.
