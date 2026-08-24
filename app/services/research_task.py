from fastapi import HTTPException


def get_research_task_by_id(task_id: int):
    if task_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="ID công việc không hợp lệ"
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