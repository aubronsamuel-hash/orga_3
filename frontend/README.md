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

### Budgets (size-limit)

Le budget de bundle (size-limit) cible `dist/assets/*.js` (build Vite). Il est execute dans le job **frontend (lint+unit+e2e-smoke)**.
Le job **frontend-storybook** ne produit que `storybook-static/` et n execute pas `size-limit`. Il fait un build et un smoke HTTP (port 6006).

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
