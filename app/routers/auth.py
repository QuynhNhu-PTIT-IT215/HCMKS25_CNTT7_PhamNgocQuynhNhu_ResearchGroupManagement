from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email đã tồn tại"
        )

    password_hash = pwd_context.hash(user.password)

    new_user = User(
        email=user.email,
        full_name=user.full_name,
        password_hash=password_hash
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user