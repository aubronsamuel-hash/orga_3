# Frontend (Jalon 12 - design system + a11y)

Base React + Vite with a small design system.

## CI local
- Installation: `npm ci`
- Lint: `npm run lint`
- Unit: `npm test`
- Storybook: `npm run storybook`
- Storybook tests: `npm run test:storybook`
- Build: `npm run build`
- Bundle budget: `npm run size`

Note: exécuter ces commandes dans `frontend/`.

### Storybook

* Build: `npm run build-storybook -- --quiet`
* Smoke CI: serveur http sur `storybook-static` puis `curl` sur `:6006`.
* Cache npm: base sur `frontend/package-lock.json` (monorepo).
