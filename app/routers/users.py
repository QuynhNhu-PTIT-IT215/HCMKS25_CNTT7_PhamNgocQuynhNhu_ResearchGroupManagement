from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.dependencies.auth import get_current_user
from app.dependencies.role import admin_required
from app.services.user import get_current_user_info, get_all_users


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return get_current_user_info(current_user)


@router.get("", response_model=list[UserResponse])
def get_users(
    search: str,
    is_active: bool,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    return get_all_users(
        db,
        search,
        is_active
    )