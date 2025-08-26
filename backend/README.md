# Backend Coulisses Crew

## Jalon 1 - Backend skeleton + healthz

### Lancer en local

```powershell
pwsh -NoLogo -NoProfile -File ../PS1/init_repo.ps1
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Ouvrir [http://localhost:8000/healthz](http://localhost:8000/healthz)

### Tests

```powershell
pytest -q backend/tests/test_healthz.py
```

### CI Gates actifs

* ruff
* mypy
* pytest

### Acceptance

* GET /healthz -> 200 JSON {"status":"ok"}
