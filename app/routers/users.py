from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse

from app.dependencies.auth import get_current_user
from app.dependencies.role import admin_required


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

#Hàm Depends(): phải chạy cái hàm trong depends trước
#sau đó mới được chạy tiếp mấy hàm ở ngoài
@router.get(
    "/me",
    response_model=UserResponse,
    summary="Lấy thông tin người dùng hiện tại",
    description="Trả về thông tin của user đang đăng nhập bằng JWT."
)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get(
    "",
    response_model=list[UserResponse],
    summary="Lấy danh sách người dùng",
    description="Chỉ Admin được xem danh sách người dùng. Có thể tìm kiếm theo tên/email và lọc trạng thái."
)
#Lý do dùng query trong search, is_active: query() dùng để khai báo
#rõ cho FastAPI rằng dữ liệu này đến từ query parameter trên URL, 
#đồng thời cho phép mình thêm mô tả, validation và các thiết lập khác.
def get_users(
    search: str = Query(None,description="Tìm kiếm theo tên hoặc email"),
    is_active: bool = Query(None,description="Lọc theo trạng thái hoạt động"),
    current_user: User = Depends(admin_required),
    db: Session = Depends(get_db)
):
    query = db.query(User)

    if search:
        query = query.filter(
            (User.full_name.contains(search)) |
            (User.email.contains(search))
        )

    if is_active is not None:
        query = query.filter(
            User.is_active == is_active
        )

    return query.all()