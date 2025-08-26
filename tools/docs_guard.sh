#!/usr/bin/env bash
set -euo pipefail
changed=$(git diff --name-only HEAD~~1 2>/dev/null | grep -E '^(backend|frontend|PS1|tools|.github)' || true)
if [[ -n "${changed}" ]]; then
    docs_changed=$(git diff --name-only HEAD~~1 2>/dev/null | grep -E '^(README.md|docs/)' || true)
    if [[ -z "${docs_changed}" ]]; then
        echo "Docs guard: changements code sans mise a jour README/docs." >&2
        exit 1
    fi
fi
echo "Docs guard OK"
