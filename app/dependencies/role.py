from fastapi import Depends, HTTPException

from app.models.user import User
from app.dependencies.auth import get_current_user


def admin_required(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Bạn không có quyền Admin"
        )

    return current_user