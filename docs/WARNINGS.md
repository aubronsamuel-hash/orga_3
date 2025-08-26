# Warnings CI — guide rapide

| Code / Message                     | Exemple / Contexte                                  | Cause probable                             | Gravite  | Action appliquee / a faire                                                                                     |
| ---------------------------------- | --------------------------------------------------- | ------------------------------------------ | -------- | -------------------------------------------------------------------------------------------------------------- |
| ruff E402                          | `Module level import not at top of file`            | Import avant configuration module-level    | Faible   | Imports reordonnes dans tests (FIXE).                                                                          |
| mypy `import-untyped` (passlib)    | `Library stubs not installed for "passlib.context"` | Pas de stubs types officiels pour passlib  | Faible   | Ignore cible: `# type: ignore[import-untyped]` + `backend/mypy.ini` limite a `passlib.*` (FIXE).               |
| `warn_unused_ignores` (mypy)       | Ignore non justifie                                 | Inline ignore redondant                    | Faible   | Maintien d’un seul ignore inline et regle `disable_error_code=import-untyped` sur `passlib.*` => pas “unused”. |
| TestClient -> httpx requis         | `RuntimeError: starlette.testclient requires httpx` | Dev dep manquante                          | Faible   | Ajout `httpx` dans `backend/requirements-dev.txt` (FIXE).                                                      |
| SQLite `PermissionError` unlink    | `WinError 32` sur cleanup \*.db                     | Handle Windows file locks                  | Faible   | `_unlink_with_retry()` dans tests (FIXE).                                                                      |
| pwsh `if exist`                    | `Missing '(' after 'if'`                            | Syntaxe CMD au lieu de PowerShell          | Faible   | Remplace par `if (Test-Path ...) { ... }` (FIXE).                                                              |
| “no such table: accounts” (pytest) | OperationalError pendant un endpoint                | Engine lie a mauvaise URL avant migrations | Majeur\* | Rebind DB dans `create_app()` via `set_database_url()` (FIXE). (*erreur runtime, pas “warning”)               |

## Politique

* **Ruff**: warnings = dette faible; on corrige immediatement si simple.
* **Mypy**: absence de stubs tiers = OK si ignore cible et documente.
* **Runtime**: toute erreur (ex. table manquante) = **bloquante** jusqu’au correctif.
* **DeprecationWarnings**: suivis dans PR mensuelle deps (voir README “Dependances”).

## Commandes utiles

```powershell
# Windows
backend\.venv\Scripts\python -m ruff check backend
backend\.venv\Scripts\python -m mypy --config-file backend\mypy.ini backend
$Env:PYTHONPATH="backend"; backend\.venv\Scripts\python -m pytest -q
```

```bash
# Linux/macOS (degrade)
PYTHONPATH=backend backend/.venv/bin/python -m ruff check backend
PYTHONPATH=backend backend/.venv/bin/python -m mypy --config-file backend/mypy.ini backend
PYTHONPATH=backend backend/.venv/bin/python -m pytest -q
```

