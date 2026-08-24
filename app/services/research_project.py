from fastapi import HTTPException


def get_research_projects():
    return {
        "success": True,
        "message": "Danh sách đề tài nghiên cứu"
    }


def get_research_project_by_id(project_id: int):
    if project_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="ID đề tài không hợp lệ"
        )

    if project_id == 403:
        raise HTTPException(
            status_code=403,
            detail="Bạn không có quyền truy cập đề tài này"
        )

    raise HTTPException(
        status_code=404,
        detail="Không tìm thấy đề tài"
    )