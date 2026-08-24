from fastapi import HTTPException
from sqlalchemy.orm import Session
from jose import JWTError

from app.models.user import User
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_refresh_token
)


def register_user(db: Session, email: str, full_name: str, password: str):
    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email đã được sử dụng"
        )

    hashed_password = get_password_hash(password)

    new_user = User(
        email=email,
        full_name=full_name,
        password_hash=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Email hoặc mật khẩu không đúng"
        )

    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Email hoặc mật khẩu không đúng"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Tài khoản đã bị khóa"
        )

    access_token = create_access_token(
        data={
            "sub": str(user.id)
        }
    )

    refresh_token = create_refresh_token(
        data={
            "sub": str(user.id)
        }
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


def refresh_access_token(db: Session, refresh_token: str):
    try:
        payload = decode_refresh_token(refresh_token)

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=401,
                detail="Refresh token không hợp lệ"
            )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Refresh token không hợp lệ"
            )

        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=401,
                detail="Refresh token không hợp lệ"
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Refresh token không hợp lệ hoặc đã hết hạn"
        )

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Người dùng không tồn tại"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Tài khoản đã bị khóa"
        )

    new_access_token = create_access_token(
        data={
            "sub": str(user.id)
        }
    )

    return {
        "access_token": new_access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }