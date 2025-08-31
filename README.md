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

Ports: BE 8000 ; FE 5173 ; DB 5432 ; Redis 6379 ; Adminer 8080 ; Prom 9090 ; Grafana 3000 ; Mailpit 8025.
Voir `deploy/README.md` pour details (compose, observabilite). Roadmap: relire `docs/roadmap.md`.

### Jalon 15.5 — Workflow d’acceptation mission
- API: /v1/invitations (create/revoke/verify), /v1/assignments/{id}/accept|decline (token ou session)
- UI: My Missions, Invite Landing (/invite?token=...)
- Tests: pytest invitations_flow, e2e Playwright acceptance (toggle par E2E_ACCEPTANCE)
### Disponibilites (Jalon 16)

* Profil user: GET/PUT /api/v1/users/{id}/profile
* Calendrier user (dispos approuvees): GET /api/v1/users/{id}/calendar?from=&to=
* Demande dispo: POST /api/v1/availabilities
* Approver/Rejecter: POST /api/v1/availabilities/{id}:approve | :reject
  Codes HTTP: 200 OK, 400 usage invalide, 404 introuvable, 409 conflit chevauchement.
  Tests:
* pwsh -NoLogo -NoProfile -File PS1/test_e2e_avail.ps1

### Conflits (Jalon 17)

* API: /api/v1/conflicts, /api/v1/conflicts/{id}, /api/v1/conflicts/resolve
* UI: /conflicts
* Tests: `pwsh -NoLogo -NoProfile -File PS1/test_backend.ps1`, `pwsh -NoLogo -NoProfile -File PS1/e2e_conflicts.ps1`
## CI

- backend: ruff, mypy, pytest
- frontend (lint+unit+e2e-smoke): build Vite + size-limit (bundle budget) + tests
- frontend-storybook: build Storybook (storybook-static/) + smoke HTTP; pas de size-limit ici car il cible dist/assets/*.js produit par le build Vite
- obs-smoke: tests ciblant observabilite (/metrics, probes)
  Relire `docs/ROADMAP.md` avant toute PR.

### Repro locale (Windows)

```powershell
pwsh -NoLogo -NoProfile -File PS1/repro_storybook_ci_cache.ps1
```

## Scripts clefs

* PS1/init_repo.ps1 : prepare venv Python et npm ci
* PS1/dev_up.ps1 : lance le stack Docker compose de dev
* PS1/dev_down.ps1 : arrete le stack compose (option -Prune pour volumes)
* PS1/smoke.ps1 : verif /healthz, /metrics et endpoint invitation
* PS1/test_all.ps1 : ruff, mypy, pytest, npm lint
* PS1/test_backend.ps1 : tests unitaires conflits
* PS1/e2e_conflicts.ps1 : e2e Playwright (conflits)
* PS1/fe_test.ps1 : npm lint, typecheck, unit
* PS1/fe_e2e.ps1 : build + e2e smoke
* tools/docs_guard.ps1 : guard doc
* tools/readme_check.ps1 : verif sections README

### Endpoint Invitations (public)

POST /api/v1/invitations/{invitation_id}/accept?token=...

* 200: { invitation_id, assignment_id, accepted: true, message }
* 400: token invalide
* 404: invitation/assignment introuvable
* 500: erreur interne

Tests:

* backend.venv\Scripts\python -m pytest -q --disable-warnings --maxfail=1

### Outils docs (Windows-first)

* PowerShell: `tools/docs_guard.ps1`, `tools/readme_check.ps1`
* Degrade Linux/macOS: `tools/docs_guard.sh`, `tools/readme_check.sh` (optionnels hors CI)

## Envs requis

Voir .env.example. Pas de secrets dans le repo. Ajout de `INVITES_SECRET` et `INVITES_TTL_SECONDS` pour les tokens d'invitation.
Variables: `VITE_API_BASE`, `PLAYWRIGHT_BASE_URL`.

## Ports

BE 8000 ; FE 5173 ; DB 5432 ; Redis 6379 ; Adminer 8080 ; Prom 9090 ; Grafana 3000 ; Mailpit 8025.

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

## CI Frontend (jalon 10)
- Le repo **n utilise pas** de workspaces npm a la racine.
- Toutes les commandes npm front s executent **dans `frontend/`**.
- Local (Windows): `pwsh -NoLogo -NoProfile -File PS1/fe_ci.ps1`

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

