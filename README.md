# Coulisses Crew (Monorepo, Jalon 4)

Badges: (CI), (coverage) a ajouter des jalons suivants.

## Quickstart Windows

```powershell
pwsh -NoLogo -NoProfile -File PS1/init_repo.ps1
pwsh -NoLogo -NoProfile -File PS1/dev_up.ps1
# Ouvrir: http://localhost:5173 et GET http://localhost:8000/api/v1/ping
```
## Quickstart Windows (compose dev)

```powershell
# lancer le stack (compose)
pwsh -NoLogo -NoProfile -File PS1/dev_up.ps1
# smoke simple
pwsh -NoLogo -NoProfile -File PS1/smoke.ps1
```

Ports: BE 8000 ; DB 5432 ; Redis 6379 ; Adminer 8080 ; Prom 9090 ; Grafana 3000 ; Mailpit 8025.
Voir `deploy/README.md` pour details (compose, observabilite). Roadmap: relire `docs/roadmap.md`.
## CI gates actifs (extrait)

* backend: ruff, mypy, pytest
* frontend: lint, typecheck, unit tests, build, e2e smoke
* obs-smoke: tests ciblant observabilite (/metrics, probes)
  Relire `docs/ROADMAP.md` avant toute PR.


## Scripts clefs

* PS1/init_repo.ps1 : prepare venv Python et npm ci
* PS1/dev_up.ps1 : lance le stack Docker compose de dev
* PS1/dev_down.ps1 : arrete le stack compose (option -Prune pour volumes)
* PS1/smoke.ps1 : verif /healthz et /metrics du backend
* PS1/test_all.ps1 : ruff, mypy, pytest, npm lint
* PS1/fe_test.ps1 : npm lint, typecheck, unit
* PS1/fe_e2e.ps1 : build + e2e smoke
* tools/docs_guard.ps1 : guard doc
* tools/readme_check.ps1 : verif sections README

### Outils docs (Windows-first)

* PowerShell: `tools/docs_guard.ps1`, `tools/readme_check.ps1`
* Degrade Linux/macOS: `tools/docs_guard.sh`, `tools/readme_check.sh` (optionnels hors CI)

## Envs requis

Voir .env.example. Pas de secrets dans le repo.

## Ports

BE 8000 ; DB 5432 ; Redis 6379 ; Adminer 8080 ; Prom 9090 ; Grafana 3000 ; Mailpit 8025.

## Cache

Un cache Redis (TTL court) couvre les listages projects/missions. Voir `backend/README.md#cache-jalon-7` pour details et tests.

## NPM registry (CI)
En CI, nous **pinnons** le fichier userconfig npm sur `frontend/.npmrc` via la variable d env `NPM_CONFIG_USERCONFIG` pour garantir l usage du **registry public**:

* Workflow: ecriture de `frontend/.npmrc` + `NPM_CONFIG_USERCONFIG=${{ github.workspace }}/frontend/.npmrc`
* Commandes:

```bash
cd frontend
npm ci --no-audit --no-fund
npm run lint
```

Astuce debug CI:

```bash
npm --version
npm config get registry
```

Si un `.npmrc` global force une registry privee, ce pin l ignore.

## Tests/Lint

```powershell
backend\.venv\Scripts\python -m ruff check backend
backend\.venv\Scripts\python -m mypy --config-file backend\mypy.ini backend
$Env$Env:PYTHONPATH="backend"; backend\.venv\Scripts\python -m pytest -q -k "v1_endpoints"
```
### Typing (passlib)

passlib n a pas de stubs officiels. Nous:

* ignorons l import dans `backend/app/auth.py` via `# type: ignore[import-untyped]`
* desactivons `import-untyped` uniquement pour `passlib.*` dans `backend/mypy.ini`

## Warnings CI

Un guide rapide est disponible dans `docs/WARNINGS.md` (codes, gravite, actions).
Scanners:

* Windows: `pwsh -NoLogo -NoProfile -File tools/warnings_scan.ps1`
* Linux/macOS: `bash tools/warnings_scan.sh`

TESTS (PS + curl):

* Windows:

  * backend.venv\Scripts\python -m ruff check backend
  * backend.venv\Scripts\python -m mypy --config-file backend\mypy.ini backend
  * $Env:PYTHONPATH="backend"; backend.venv\Scripts\python -m pytest -q
  * pwsh -NoLogo -NoProfile -File PS1/fe_test.ps1
  * pwsh -NoLogo -NoProfile -File PS1/fe_e2e.ps1
* Linux/macOS:

  * PYTHONPATH=backend backend/.venv/bin/python -m pytest -q
  * cd frontend && npm ci && npm run lint && npm run typecheck && npm run test:unit && npm run build && npm run test:e2e

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

