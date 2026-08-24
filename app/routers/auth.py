from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import RefreshTokenRequest, TokenResponse
from app.services.auth import register_user,login_user,refresh_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate,db: Session = Depends(get_db)):
    return register_user(db,user.email,user.full_name,user.password)


@router.post("/login", response_model=TokenResponse)
def login(email: str,password: str,db: Session = Depends(get_db)):
    return login_user(db,email,password)


@router.post("/refresh", response_model=TokenResponse)
def refresh(data: RefreshTokenRequest,db: Session = Depends(get_db)):
    return refresh_access_token(db,data.refresh_token)

@router.post("/refresh", response_model=TokenResponse)
def refresh(data: RefreshTokenRequest,db: Session = Depends(get_db)):
    return refresh_access_token(db,data.refresh_token)