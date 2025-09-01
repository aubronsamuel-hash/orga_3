from __future__ import annotations

import os
import subprocess
import sys


def main() -> int:
    os.chdir("backend")
    os.environ["MYPYPATH"] = "typing_stubs"
    cmd = [sys.executable, "-m", "mypy", "--config-file", "../mypy.ini", "app", "tests"]
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())

