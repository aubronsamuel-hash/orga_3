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

## Jalon 3 - Modeles metier

### Enums

* assignment_status: INVITED | ACCEPTED | DECLINED | CANCELLED
* project_status: DRAFT | ACTIVE | ARCHIVED

### Tables (principales)

* orgs, accounts, users (+ skills, tags), projects, missions (+ roles), assignments, availability, invitations, audit_log.

### Contraintes clefs

* Unicite assignment actif par (mission_id, user_id): index unique partiel sur status IN ('INVITED','ACCEPTED')

### Tests

```powershell
$Env:PYTHONPATH="backend"
backend\.venv\Scripts\python -m pytest -q backend/tests/test_models_crud.py
backend\.venv\Scripts\python -m pytest -q backend/tests/test_assignments_uniqueness.py
```

### Alembic

```powershell
$Env:DATABASE_URL="sqlite:///./backend/dev.db"
backend\.venv\Scripts\alembic -c backend\alembic.ini upgrade head
```

## Jalon 4 - Auth reelle (JWT + refresh)

### Endpoints

* POST /api/v1/auth/login  -> JSON {access_token}, cookie httpOnly refresh_token
* POST /api/v1/auth/refresh -> JSON {access_token} (lit cookie refresh)
* POST /api/v1/auth/logout  -> supprime le cookie
* GET  /api/v1/auth/me      -> infos compte derivees du JWT
* POST /api/v1/auth/reset/request -> en dev renvoie {reset_token}
* POST /api/v1/auth/reset/confirm -> applique le nouveau mot de passe

### Variables env

* SECRET_KEY, JWT_ALG, ACCESS_TOKEN_MINUTES, REFRESH_TOKEN_DAYS

### Notes CORS/CSRF

* Refresh utilise un cookie httpOnly SameSite=Lax. En prod, mettre Secure=True via TLS et ajouter un CSRF header si necessaire.
* Ce jalon ne couvre pas l envoi email (fait plus tard). En dev, le token de reset est renvoye dans la reponse.

### Tests

```powershell
$Env:PYTHONPATH="backend"
backend\.venv\Scripts\python -m pytest -q backend/tests/test_auth_flow.py
backend\.venv\Scripts\python -m pytest -q backend/tests/test_password_reset_flow.py
```

### Note DB pour les tests (robustesse ordre d import)

L app utilise une **factory** `create_app()` qui rebinde l engine/Session sur `DATABASE_URL` courant via `set_database_url()` (dans `app.db`).
Cela evite les erreurs type `no such table: accounts` quand un autre test importe l app avant d avoir positionne `DATABASE_URL`.

### Tests

```powershell
$Env:PYTHONPATH="backend"
backend\.venv\Scripts\python -m pytest -q
```

ou

```bash
PYTHONPATH=backend backend/.venv/bin/python -m pytest -q
```

## RBAC (Jalon 5)

* Table `org_memberships`: (id, org_id, account_id, role: owner|admin|manager|tech)
* Enforcement:
  * `require_role(min_role)` -> verifie qu'un account est membre de l'org du token et que son role >= min_role
  * `require_org_scope(org_id)` -> verifie que l'org_id du path == claim `org`
* Endpoints de demo (pour tests):
  * GET `/api/v1/rbac_demo/any` (membre requis)
  * GET `/api/v1/rbac_demo/manager` (>= manager)
  * GET `/api/v1/rbac_demo/admin` (>= admin)
  * GET `/api/v1/rbac_demo/owner` (== owner)
  * GET `/api/v1/rbac_demo/scoped/{org_id}` (scope org strict)
* Tests:

```powershell
$Env:PYTHONPATH="backend"
backend\.venv\Scripts\python -m pytest -q -k "rbac"
```

* Matrice roles x actions minimale: owner > admin > manager > tech. Les endpoints metier (Jalon 6) utiliseront ces deps pour le controle fin. (Roadmap Jalon 5-6).

## API v1 (Jalon 6)

Endpoints exposes (subset prioritaire) :

* `/api/v1/projects` CRUD + `/{id}/missions:bulk_create`
* `/api/v1/missions` CRUD de base + `/{id}:duplicate`
* `/api/v1/assignments` CRUD + `/{id}:status` (ACCEPTED/DECLINED/...)
* `/api/v1/invitations` create/revoke + `/{id}/accept|decline?token=...` (token signe typ=invite)
* `/api/v1/users` CRUD minimal + recherche
* `/api/v1/availability` CRUD simple
* `/api/v1/conflicts/user/{uid}` detection overlaps affectations ACCEPTED
* `/api/v1/rates/user/{uid}` get/set profil tarifaire
* `/api/v1/orgs/members` liste membres + roles
  Ecriture: `require_role(Role.manager)` ; Lecture: `require_role(Role.tech)` par defaut.
  Flux cle: invitation -> accept/decline met a jour `assignments.status`. (Roadmap Jalon 6)

### Codes d erreur

* 400: validations (ex: conflit horaire)
* 401/403: auth/rbac
* 404: introuvable

### Tests

```powershell
$Env:PYTHONPATH="backend"
backend\.venv\Scripts\python -m pytest -q -k "v1_endpoints"
```

ACCEPTANCE:

* CRUD de base projects/missions/users/assignments OK.
* `projects/{id}/missions:bulk_create` cree plusieurs missions.
* `invitations create` renvoie un token; `accept` et `decline` changent `assignments.status` (OK et KO couverts).
* `assignments:{id}:status` refuse ACCEPTED en cas de conflit horaire.
* `conflicts/user/{uid}` retourne les overlaps pour ACCEPTED.
* CI verte (ruff/mypy/pytest). Viser >=70% de cov pour ce jalon (selon roadmap).
