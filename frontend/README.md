# Frontend (Jalon 10)

Socle React+Vite+TS+Tailwind + Router, ESLint, Vitest, Playwright, Storybook. Shell UI pret. 

## Quickstart (Windows)

```powershell
cd frontend
npm ci --registry=https://registry.npmjs.org/ --no-audit --no-fund
npm run dev
```

## Scripts

* `npm run lint` / `npm run typecheck`
* `npm run test` (Vitest) / `npm run test:unit`
* `npm run test:e2e` (Playwright) / `test:e2e:ci`
* `npm run storybook` / `npm run build-storybook`
* `npm run build` / `npm run preview`

## Theming

Bouton ThemeToggle (light/dark) ajoute une classe `dark` sur `<html>`. Layout basique avec header, routes Home/Login/404.

## Tests

* Unit: Vitest + Testing Library.
* E2E: Playwright smoke charge la home et verifie le header.

## CI Gates (frontend)

Lint, typecheck, unit tests, e2e smoke. 
