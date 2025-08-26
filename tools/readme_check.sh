#!/usr/bin/env bash
set -euo pipefail
content="$(cat README.md 2>/dev/null || true)"
missing=0
for s in "Quickstart Windows" "Scripts clefs" "Envs requis" "Ports" "Tests/Lint" "FAQ" "Badges" "README Policy" "Dependances et lockfiles"; do
    if ! grep -qF "$s" <<<"$content"; then
        echo "README incomplet: section manquante: $s" >&2
        missing=1
    fi
done
[[ $missing -eq 0 ]] && echo "README structure OK" || exit 1
