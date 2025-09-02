# syntax=docker/dockerfile:1

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    SAFE_MODE=1

WORKDIR /app

# Deps minimales pour SAFE_MODE (/healthz)

# Pins stables pour reproductibilite CI

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir fastapi==0.115.0 uvicorn==0.30.6

# Code backend (routes lourdes protegees par SAFE_MODE)

COPY backend/ backend/

EXPOSE 8000
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
