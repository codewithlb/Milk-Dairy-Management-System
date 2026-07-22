from fastapi import Depends, HTTPException

from app.dependencies.auth import get_current_admin


def require_admin(current_admin=Depends(get_current_admin)):
    return current_admin


def require_superadmin(current_admin=Depends(get_current_admin)):
    if current_admin.get("role") != "superadmin":
        raise HTTPException(
            status_code=403,
            detail="Only Super Admin can access this resource."
        )

    return current_admin