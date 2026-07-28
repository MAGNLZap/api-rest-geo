# Stage 1: builder - install dependencies with gcc
FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

COPY requirements-base.txt requirements-prod.txt ./
RUN pip install --no-cache-dir --prefix=/install -r requirements-base.txt -r requirements-prod.txt

# Stage 2: runtime - minimal image without gcc
FROM python:3.12-slim AS runtime

WORKDIR /app

COPY --from=builder /install /usr/local

COPY app/ ./app/
COPY scripts/ ./scripts/
COPY data/ ./data/

RUN adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8001

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
