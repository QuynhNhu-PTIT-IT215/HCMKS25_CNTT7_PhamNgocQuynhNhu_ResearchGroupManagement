from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse

from app.core.dependencies import (
    get_current_user,
    admin_required
)


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user


@router.get("", response_model=list[UserResponse])
def get_users(
    search: str = None,
    is_active: bool = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    query = db.query(User)

    if search:
        query = query.filter(
            (User.full_name.ilike(f"%{search}%")) |
            (User.email.ilike(f"%{search}%"))
        )

    if is_active is not None:
        query = query.filter(
            User.is_active == is_active
        )

    return query.all()