from __future__ import annotations

from fastapi import APIRouter, Depends

from .rbac import Role, require_org_scope, require_role

router = APIRouter(prefix="/api/v1/rbac_demo", tags=["rbac-demo"])


@router.get("/any")
def any_member(_ctx=Depends(require_role(Role.tech))) -> dict[str, bool | str]:
    return {"ok": True, "need": "tech"}


@router.get("/manager")
def only_manager_plus(_ctx=Depends(require_role(Role.manager))) -> dict[str, bool | str]:
    return {"ok": True, "need": "manager+"}


@router.get("/admin")
def only_admin_plus(_ctx=Depends(require_role(Role.admin))) -> dict[str, bool | str]:
    return {"ok": True, "need": "admin+"}


@router.get("/owner")
def only_owner(_ctx=Depends(require_role(Role.owner))) -> dict[str, bool | str]:
    return {"ok": True, "need": "owner"}


@router.get("/scoped/{org_id}")
def scoped(_=Depends(require_org_scope)) -> dict[str, bool | str]:
    return {"ok": True, "scope": "org"}
