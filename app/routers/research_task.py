from fastapi import APIRouter, HTTPException


router = APIRouter(
    prefix="",
    tags=["Research Task"]
)


@router.get("/research-tasks/{task_id}")
def get_research_task(task_id: int):

    if task_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Mã công việc không hợp lệ"
        )

    if task_id == 403:
        raise HTTPException(
            status_code=403,
            detail="Bạn không có quyền truy cập công việc này"
        )

    raise HTTPException(
        status_code=404,
        detail="Không tìm thấy công việc"
    )