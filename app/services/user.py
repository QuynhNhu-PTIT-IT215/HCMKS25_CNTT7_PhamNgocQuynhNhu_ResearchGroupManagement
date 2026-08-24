from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User


def get_current_user_info(current_user: User):
    return current_user


def get_all_users(
    db: Session,
    search: str,
    is_active: bool
):
    query = db.query(User)

    if search:
        query = query.filter(
            (User.full_name.like(f"%{search}%")) |
            (User.email.like(f"%{search}%"))
        )

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    users = query.all()

    return users