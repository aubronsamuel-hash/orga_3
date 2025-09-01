#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../frontend"
export NODE_OPTIONS="--max-old-space-size=4096"
npm ci
npx storybook build
echo "[OK] Storybook built at frontend/storybook-static"
