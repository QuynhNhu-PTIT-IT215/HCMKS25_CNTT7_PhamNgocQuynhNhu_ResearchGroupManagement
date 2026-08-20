from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me")
def get_me():
    raise HTTPException(
        status_code=404,
        detail="Không tìm thấy người dùng"
    )


@router.get("")
def get_users():
    raise HTTPException(
        status_code=403,
        detail="Bạn không có quyền xem danh sách người dùng"
    )