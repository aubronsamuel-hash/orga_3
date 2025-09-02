#!/usr/bin/env python
from __future__ import annotations

import os
import sys
from pathlib import Path
from mypy import api as mypy_api

ROOT = Path(__file__).resolve().parent.parent
BACKEND = ROOT / "backend"
CONFIG = BACKEND / "mypy.ini"

# Forcer la resolution pour le package "backend"
os.environ.setdefault("MYPYPATH", str(BACKEND))
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

targets = [str(BACKEND / "app")]
bt = BACKEND / "tests"
rt = ROOT / "tests"
if bt.exists():
    targets.append(str(bt))
if rt.exists():
    targets.append(str(rt))

args = ["--config-file", str(CONFIG)] + targets
stdout, stderr, status = mypy_api.run(args)

# Rejoue la sortie comme la CI attend
if stdout:
    print(stdout, end="")
if stderr:
    print(stderr, end="", file=sys.stderr)
raise SystemExit(status)

