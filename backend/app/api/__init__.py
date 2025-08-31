# Sous-package api

from __future__ import annotations

from fastapi import APIRouter
from typing import List

router = APIRouter(prefix="/api/v1")

@router.get("/ping")
def ping() -> dict[str, str]:
    return {"status": "ok"}

__all__: List[str] = []
