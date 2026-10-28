---
description: Inicia el servidor de desarrollo
agent: build
---

Inicia FastAPI usando `HOST`, `PORT` y modo reload desde `.env`:

```pwsh
python -m app.main
```

No dejes procesos duplicados. Si el puerto está ocupado, informa el PID antes de iniciar otro servidor.
