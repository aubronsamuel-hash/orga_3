# Package app (py.typed pour mypy/peps)

# fichier volontairement minimal

__all__: list[str] = []

# Indiquer a mypy que le package est type-hinte (si vous avez un fichier py.typed, gardez-le)
try:
    import importlib.resources as _res  # noqa: F401
except Exception:
    pass

