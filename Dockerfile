# syntax=docker/dockerfile:1

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    SAFE_MODE=1

WORKDIR /app

# Deps minimales pour servir /healthz

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir fastapi==0.115.0 uvicorn==0.30.6

# Code necessaire

COPY deploy/ deploy/
COPY backend/ backend/

EXPOSE 8000

# Si SAFE_MODE=1 => micro-app /healthz (independante du backend)
# Sinon => backend complet

CMD ["/bin/sh","-lc","if [ \"$SAFE_MODE\" = \"1\" ]; then uvicorn deploy.k6.health_app:app --host 0.0.0.0 --port 8000; else uvicorn backend.app.main:app --host 0.0.0.0 --port 8000; fi"]
