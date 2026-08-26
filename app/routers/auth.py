from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.auth import (
    UserLogin,
    TokenResponse,
    RefreshTokenRequest
)

from app.schemas.user import UserCreate

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

    return register_user(
        db,
        user.email,
        user.full_name,
        user.password
    )


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

    return login_user(
        db,
        user.email,
        user.password
    )


@router.post(
    "/token",
    response_model=TokenResponse,
    summary="Đăng nhập Swagger",
    description="Đăng nhập bằng form để Swagger Authorize nhận JWT."
)
def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    return login_user(
        db,
        form_data.username,
        form_data.password
    )


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