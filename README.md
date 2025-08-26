# Coulisses Crew (Monorepo, Jalon 0)

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

## Envs requis

Voir .env.example. Pas de secrets dans le repo.

## Ports

BE 8000 ; FE 5173 ; DB 5432 ; Redis 6379 ; Adminer 8080.

## Tests/Lint

```powershell
pwsh -NoLogo -NoProfile -File PS1/test_all.ps1
```

## README Policy

Tout changement de CLI/API/env/scripts/ports/procedures => MAJ README(s) concernes (root + dossiers). CI docs guard echoue si non mis a jour.

## FAQ

Q: Ca ne demarre pas ?
R: Verifier python, npm et l existance du venv. Utiliser dev_down.ps1 puis dev_up.ps1.
