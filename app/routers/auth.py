from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.auth import (
    UserCreate,
    UserLogin,
    TokenResponse,
    RefreshTokenRequest
)
from app.services.auth import (
    register_user,
    login_user,
    refresh_access_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=201,
    summary="Đăng ký tài khoản",
    description="Tạo tài khoản người dùng mới."
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return register_user(db, user)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Đăng nhập",
    description="Xác thực email và mật khẩu để nhận JWT access token."
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    return login_user(db, user)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Làm mới access token",
    description="Sử dụng refresh token để cấp access token mới."
)
def refresh(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    return refresh_access_token(
        db,
        data.refresh_token
    )