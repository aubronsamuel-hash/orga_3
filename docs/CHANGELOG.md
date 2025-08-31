# Changelog

## [Unreleased]
### Added
- Jalon 15.5: workflow d’acceptation (API, UI, tokens signés, tests)

## Jalon 12 – Design system + a11y
- Added CSS tokens and theme variables.
- Integrated base UI components with stories.
- Global focus rings and keyboard shortcuts.
- CI checks: Storybook build, a11y tests, bundle budget.

## Jalon 13 – Data fetching et état
- HTTP client avec retries et CSRF.
- Gestion d'état avec TanStack Query et Zustand.
- Update optimiste et route /dev/retry pour tests.

## Jalon 15.5 – Workflow acceptation mission
- Service de tokens d'invitation (HMAC, expiration).
- Table `invitations` avec hash de token.
