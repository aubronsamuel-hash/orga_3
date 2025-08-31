# Style Guide

This project uses a small design system based on CSS variables and basic UI components.

## Tokens
- Colors, spacing, radius, shadow and ring are defined in `frontend/src/styles/tokens.css`.
- `frontend/src/styles/theme.css` applies light and dark themes via `prefers-color-scheme`.
- Tailwind is configured to read these CSS variables.

## Components
Reusable components are available under `frontend/src/components/ui`:
- `Button`
- `Input`
- `Table`
- `Dialog`
- `Toast`

Each component includes accessibility friendly defaults and stories in Storybook.

## Conventions
- Visible focus rings use the `:focus-visible` selector with the `--ring` token.
- Global keyboard shortcuts: `Ctrl/Cmd+K` opens the command menu, `?` shows help.
