from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.research_task import (
    ResearchTaskResponse,
    ResearchTaskUpdate
)

from app.services.research_task import (
    get_research_task_by_id,
    update_research_task,
    delete_research_task
)

from app.schemas.research_task import (
    ResearchTaskCreate,
    ResearchTaskResponse
)

from app.services.research_task import (
    create_research_task,
    get_research_tasks
)


router = APIRouter(
    prefix="/research-tasks",
    tags=["Research Tasks"]
)


@router.get(
    "/{task_id}",
    response_model=ResearchTaskResponse,
    summary="Lấy nhiệm vụ nghiên cứu",
    description="Chỉ thành viên của đề tài chứa nhiệm vụ mới được xem."
)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_research_task_by_id(
        db,
        task_id,
        current_user.id
    )


@router.patch(
    "/{task_id}",
    response_model=ResearchTaskResponse,
    summary="Cập nhật nhiệm vụ nghiên cứu",
    description="Owner hoặc assignee có thể cập nhật các trường hợp lệ. Các trường không gửi sẽ được giữ nguyên."
)
def update_task(
    task_id: int,
    task: ResearchTaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return update_research_task(
        db,
        task_id,
        current_user.id,
        task
    )


@router.delete(
    "/{task_id}",
    status_code=200,
    summary="Xóa nhiệm vụ nghiên cứu",
    description="Chỉ Owner của đề tài mới được xóa nhiệm vụ nghiên cứu."
)
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return delete_research_task(
        db,
        task_id,
        current_user.id
    )

@router.post(
    "/{project_id}/research-tasks",
    response_model=ResearchTaskResponse,
    status_code=201,
    summary="Tạo nhiệm vụ nghiên cứu",
    description="Thành viên của đề tài có thể tạo nhiệm vụ nghiên cứu."
)
def create_task(
    project_id: int,
    task: ResearchTaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_research_task(
        db,
        project_id,
        current_user.id,
        task
    )


@router.get(
    "/{project_id}/research-tasks",
    response_model=list[ResearchTaskResponse],
    summary="Lấy danh sách nhiệm vụ nghiên cứu",
    description="Lấy các nhiệm vụ thuộc đề tài mà user hiện tại có quyền truy cập."
)
def get_tasks(project_id: int,
    status: str = Query(None,description="Lọc theo status: TODO, IN_PROGRESS, DONE"),
    priority: str = Query(None,description="Lọc theo priority: LOW, MEDIUM, HIGH"),
    assignee_id: int = Query(None,description="Lọc theo người được giao"),
    search: str = Query(None,description="Tìm kiếm theo title"),
    limit: int = Query(10,ge=1,le=100,description="Số lượng nhiệm vụ trả về"),
    offset: int = Query(0,ge=0,description="Số lượng nhiệm vụ bỏ qua"),
    sort_by: str = Query("created_at",description="Sắp xếp theo created_at hoặc due_date"),
    sort_order: str = Query("desc",description="Thứ tự sắp xếp: asc hoặc desc"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_research_tasks(
        db,
        project_id,
        current_user.id,
        status,
        priority,
        assignee_id,
        search,
        limit,
        offset,
        sort_by,
        sort_order
    )
