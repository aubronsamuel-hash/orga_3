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

### Imports et PYTHONPATH

Les tests importent app.main. Il faut que backend/ soit dans PYTHONPATH.

* En local, c est gere par backend/conftest.py.
* En CI et scripts PS1, on exporte PYTHONPATH=backend avant pytest.

### CI Gates actifs

* ruff
* mypy
* pytest

### Acceptance

* GET /healthz -> 200 JSON {"status":"ok"}
