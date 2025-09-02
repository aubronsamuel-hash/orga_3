#!/usr/bin/env python
from __future__ import annotations

import os
import sys
from pathlib import Path
from mypy import api as mypy_api

ROOT = Path(__file__).resolve().parent.parent
BACKEND = ROOT / "backend"
CONFIG = BACKEND / "mypy.ini"

# Unifier la resolution: racine repo sur sys.path, pas de MYPYPATH=backend
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.environ.pop("MYPYPATH", None)  # evite mapping app.* fantome

# Cible: le package "backend" (avec bases explicites)
targets = ["backend"]

args = ["--config-file", str(CONFIG), "--explicit-package-bases"] + targets
stdout, stderr, status = mypy_api.run(args)
if stdout:
    print(stdout, end="")
if stderr:
    print(stderr, end="", file=sys.stderr)
raise SystemExit(status)

