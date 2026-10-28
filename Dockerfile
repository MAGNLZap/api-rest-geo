FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENVIRONMENT=production \
    ALLOW_LOCAL_NETWORK=false \
    FORWARDED_ALLOW_IPS=127.0.0.1

COPY requirements.txt ./
RUN pip install --no-cache-dir --no-compile -r requirements.txt

RUN addgroup --system app && \
    adduser --system --ingroup app app && \
    chown app:app /app

COPY --chown=app:app app/ ./app/
COPY --chown=app:app demo/index.html ./demo/index.html
COPY --chown=app:app demo/ua_amenazas.html ./demo/ua_amenazas.html
COPY --chown=app:app demo/unidades_infancia.html ./demo/unidades_infancia.html
USER app

EXPOSE 8001

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import os, urllib.request; urllib.request.urlopen(f'http://127.0.0.1:{os.getenv(\"PORT\", \"8001\")}/health', timeout=3)"]

CMD ["python", "-m", "app.main"]
