# Backend Coulisses Crew

## Jalon 1 - Backend skeleton + healthz

* GET /healthz -> 200 JSON {"status":"ok"}

## Jalon 2 - DB + Alembic

Objectif: initialiser SQLAlchemy + Alembic, fournir une premiere migration et valider upgrade/downgrade.

### URLs de base

* DATABASE_URL (env) prioritaire.
* Par defaut au jalon 2 (sans Postgres): `sqlite:///./backend/dev.db`

### Commandes Alembic (PowerShell)

```powershell
# Upgrade head (utilise DATABASE_URL si defini, sinon SQLite)
$Env:DATABASE_URL="sqlite:///./backend/dev.db"
backend\.venv\Scripts\alembic -c backend\alembic.ini upgrade head

# Downgrade base
backend\.venv\Scripts\alembic -c backend\alembic.ini downgrade base
```

### Tests

```powershell
# Teste upgrade/downgrade sur un fichier SQLite temporaire
PYTHONPATH=backend backend\.venv\Scripts\python -m pytest -q backend/tests/test_migrations.py
```

### CI Gates actifs

* ruff, mypy, pytest (incluant test_migrations)

### Notes

* Cible finale: Postgres 16 (avec Docker compose au Jalon 9). Au jalon 2, la CI s appuie sur SQLite pour des tests deterministes.
* A partir du Jalon 3, les modeles metier seront introduits et les migrations evoluent.
