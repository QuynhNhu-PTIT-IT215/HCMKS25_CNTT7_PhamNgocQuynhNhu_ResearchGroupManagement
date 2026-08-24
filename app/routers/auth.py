from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.auth import register_user, login_user


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate,db: Session = Depends(get_db)):
    return register_user(db,user.email,user.full_name,user.password)


@router.post("/login")
def login(email: str,password: str,db: Session = Depends(get_db)):
    return login_user(db,email,password)