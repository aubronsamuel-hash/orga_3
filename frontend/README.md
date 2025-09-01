# Frontend (Jalon 13 - data fetching et état)

Base React + Vite with a small design system.

## Data fetching et etat

- TanStack Query: queryClient, retry=2, staleTime=30s
- Helpers `useApiQuery` / `useApiMutation`
- Update optimiste (`useUpdateProfile`)
- Route test `/dev/retry` pour e2e

## Calendrier (J14)

- Vues: Month / Week / Day (FullCalendar) + Timeline simple (CSS Grid).
- DnD: drag & drop et resize.
- Filtres: status, user/org/project. Timezone.
- Tests e2e: `npm -w frontend run e2e:ci` (spec: calendar-dnd).
- Bundle budget: `npm -w frontend run size`.

## CI

- Installation: `npm ci`
- Lint: `npm run lint`
- Unit: `npm run test:unit`
- Storybook: `npm run storybook`
- Storybook tests: `npm run test:storybook`
- Build: `npm run build`
- Bundle budget: `npm run size`

Note: executer ces commandes dans `frontend/`.

## Storybook

### Scripts

* npm run storybook : lance Storybook dev
* npm run build:storybook : compile le site statique
* npm run chromatic : publie sur Chromatic (requis: CHROMATIC_PROJECT_TOKEN)

### Storybook tests

* `npm run test:storybook` : lance les tests end-to-end des stories (Playwright).
* `npm run test:storybook:static` : teste contre `storybook-static` servi en local.
* Desactiver un test pour une story lourde: ajouter `parameters: { test: { disable: true } }` dans la story.

### Secrets

* CHROMATIC_PROJECT_TOKEN : a definir dans GitHub Secrets pour activer la publication CI.

### Budgets (size-limit)

Le budget de bundle (size-limit) cible `dist/assets/*.js` (build Vite). Il est execute dans le job **frontend (lint+unit+e2e-smoke)**.
Le job **storybook** publie via Chromatic (non bloquant, Phase 1) et n'exécute pas `size-limit`.

## Repro Storybook (Windows)

```
pwsh -NoLogo -NoProfile -File ..\PS1\repro_storybook_ci_cache.ps1
```

## Acceptance workflow

```
npm run dev
# e2e acceptance toggle
$Env:E2E_ACCEPTANCE=1; npm run e2e
```

## Page Conflits

Route `/conflicts`: liste des conflits detectes; clic sur "Remplacer par X" tente une resolution et retire le conflit si OK.
