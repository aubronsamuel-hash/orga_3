# Dev stack (compose)

Roadmap J9: compose dev avec backend, pg, redis, grafana, loki, prometheus, mailpit. Acceptance: app up via compose; CLI docker smoke.

## Prerequis

* Docker Desktop (engine Linux) sur Windows.
* Fichier `.env` a partir de `.env.example` (valeurs demo OK, pas de secret en clair).

## Demarrage (Windows)

```powershell
pwsh -NoLogo -NoProfile -File PS1/dev_up.ps1
# Smoke local
pwsh -NoLogo -NoProfile -File PS1/smoke.ps1
```

## Services

* Backend: http://localhost:8000
* Prometheus: http://localhost:9090
* Grafana: http://localhost:3000 (admin/admin)
* Loki: 3100
* Mailpit: http://localhost:8025 (SMTP 1025)
* Adminer: http://localhost:8080
* Postgres: localhost:5432 (DB ${POSTGRES_DB}, user ${POSTGRES_USER})

### Note image backend
L image definit `ENV PYTHONPATH=/app/backend` afin que `uvicorn app.main:create_app` importe correctement le package `app` situe sous `/app/backend`. Sans cela, le process tomberait au demarrage (import error) et le port 8000 ne repondrait pas en smoke.

## Arret

```powershell
pwsh -NoLogo -NoProfile -File PS1/dev_down.ps1
# avec purge volumes nommes
pwsh -NoLogo -NoProfile -File PS1/dev_down.ps1 -Prune
```
