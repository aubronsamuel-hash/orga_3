# Frontend (Jalon 11 - Auth)

Flux auth FE complet: login/logout, refresh auto 401, gardes de routes protegees. Session via cookies httpOnly (fetch avec `credentials: include`). En-tete CSRF: meta `csrf-token` dans `index.html`.

## Quickstart (Windows)

```powershell
cd frontend
npm ci --registry=https://registry.npmjs.org/ --no-audit --no-fund
npm run dev
```

## Variables

* `VITE_API_BASE` (defaut `/api/v1`)

## API client

* Intercepte 401 -> POST `/auth/refresh` -> retry.
* Headers: `Content-Type: application/json` si body, `X-CSRF` depuis meta `csrf-token`.

## Composants

* `AuthProvider`: charge `/auth/me`, expose `login`, `logout`.
* `Protected`: redirige vers `/login` si non auth.
* `Dashboard`: bouton "Charger projets" pour illustrer un appel protege (avec refresh si 401).

## Tests e2e (Playwright)

Mock reseau via `page.route("**/api/v1/**", ...)`:

* `/auth/me`: 401 -> apres login: 200
* `/auth/login`: 200
* `/auth/refresh`: 200
* `/projects`: 401 une fois puis 200 (verifie le refresh)
  Commandes:

```bash
cd frontend
npm run build
npx playwright install --with-deps
npm run test:e2e
```

## CMD_TESTS

# Windows

pwsh -NoLogo -NoProfile -File PS1/fe_test.ps1
pwsh -NoLogo -NoProfile -File PS1/fe_e2e.ps1

# Linux/mac

cd frontend && npm ci && npm run lint && npm run typecheck && npm run test:unit && npm run build && npm run test:e2e

## ACCEPTANCE

* Aller sur /app non connecte -> redir /login.
* Login OK -> redirect /app, "Bonjour <email>" visible.
* Clic "Charger projets": premier appel 401 -> refresh -> retry 200 -> "Projets: 1".
* CI frontend verts (lint/typecheck/unit/build/e2e).

## GIT

Branche feat/jalon-11-frontend-auth
PR "Jalon 11 - Frontend auth (login/logout, refresh, gardes, e2e)"
Commit feat(fe-auth): API client + AuthProvider + Protected + Login + Dashboard + e2e
Labels: build, tests, docs-required
