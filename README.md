# Coulisses Crew (Monorepo, Jalon 4)

Badges: (CI), (coverage) a ajouter des jalons suivants.

## Quickstart Windows

```powershell
pwsh -NoLogo -NoProfile -File PS1/init_repo.ps1
pwsh -NoLogo -NoProfile -File PS1/dev_up.ps1
# Ouvrir: http://localhost:5173 et GET http://localhost:8000/api/v1/ping
```

## Scripts clefs

* PS1/init_repo.ps1 : prepare venv Python et npm ci
* PS1/dev_up.ps1 : lance uvicorn et vite
* PS1/dev_down.ps1 : arrete uvicorn/node
* PS1/smoke.ps1 : verif API /api/v1/ping
* PS1/test_all.ps1 : ruff, mypy, pytest, npm lint
* tools/docs_guard.ps1 : guard doc
* tools/readme_check.ps1 : verif sections README

### Outils docs (Windows-first)

* PowerShell: `tools/docs_guard.ps1`, `tools/readme_check.ps1`
* Degrade Linux/macOS: `tools/docs_guard.sh`, `tools/readme_check.sh` (optionnels hors CI)

## Envs requis

Voir .env.example. Pas de secrets dans le repo.

## Ports

BE 8000 ; FE 5173 ; DB 5432 ; Redis 6379 ; Adminer 8080.

## Tests/Lint

```powershell
backend\.venv\Scripts\python -m ruff check backend
backend\.venv\Scripts\python -m mypy --config-file backend\mypy.ini backend
$Env:PYTHONPATH="backend"; backend\.venv\Scripts\python -m pytest -q -k "v1_endpoints"
```
### Typing (passlib)

passlib n a pas de stubs officiels. Nous:

* ignorons l import dans `backend/app/auth.py` via `# type: ignore[import-untyped]`
* desactivons `import-untyped` uniquement pour `passlib.*` dans `backend/mypy.ini`

## README Policy

Tout changement de CLI/API/env/scripts/ports/procedures => MAJ README(s) concernes (root + dossiers). CI docs guard echoue si non mis a jour.

## Dependances et lockfiles

Les lockfiles sont obligatoires (policy DEPENDANCES).

### Backend (dev)

* Runtime: `backend/requirements.txt` (inclut `email-validator` requis par `pydantic.EmailStr`)
* Dev (CI lints/tests): `backend/requirements-dev.txt`

Deps dev incluent `httpx` pour `fastapi.testclient`:

```powershell
backend\.venv\Scripts\pip install -r backend\requirements.txt -r backend\requirements-dev.txt
```

### Frontend

* `frontend/package-lock.json` doit etre committe.

```powershell
pwsh -NoLogo -NoProfile -File PS1/gen_frontend_lock.ps1
git add frontend/package-lock.json
git commit -m "chore(frontend): regen package-lock"
```

La CI utilise `npm ci` et echouera si le lockfile est absent.

## FAQ

Q: Ca ne demarre pas ?
R: Verifier python, npm et l existance du venv. Utiliser dev_down.ps1 puis dev_up.ps1.
