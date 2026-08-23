from fastapi import APIRouter, HTTPException


router = APIRouter(
    prefix="",
    tags=["Research Project"]
)


@router.get("/research-projects/{project_id}")
def get_research_project(project_id: int):

    if project_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Mã đề tài không hợp lệ"
        )

    if project_id == 403:
        raise HTTPException(
            status_code=403,
            detail="Bạn không có quyền truy cập đề tài này"
        )

    raise HTTPException(
        status_code=404,
        detail="Không tìm thấy đề tài nghiên cứu"
    )


@router.get("/research-projects")
def get_research_projects():

    return {
        "message": "Danh sách đề tài nghiên cứu"
    }
