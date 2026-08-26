from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.research_project import (
    ResearchProjectCreate,
    ResearchProjectResponse,
    ResearchProjectUpdate,
    ResearchMemberCreate,
    ResearchMemberResponse
)

from app.schemas.research_task import (
    ResearchTaskCreate,
    ResearchTaskResponse
)

from app.services.research_project import (
    create_research_project,
    get_research_projects,
    get_research_project_by_id,
    update_research_project,
    delete_research_project,
    add_research_member,
    delete_research_member,
    get_research_project_members
)

from app.services.research_task import (
    create_research_task,
    get_research_tasks
)


router = APIRouter(
    prefix="/research-projects",
    tags=["Research Projects"]
)


@router.post(
    "",
    response_model=ResearchProjectResponse,
    status_code=201,
    summary="Tạo đề tài nghiên cứu",
    description="User đăng nhập tạo một đề tài nghiên cứu mới và trở thành Owner."
)
def create_project(
    project: ResearchProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_research_project(
        db,
        current_user.id,
        project.name,
        project.description
    )


@router.get(
    "",
    summary="Lấy danh sách đề tài nghiên cứu",
    description="Lấy các đề tài mà user hiện tại là Owner hoặc Member. Có thể tìm kiếm theo tên."
)
def get_projects(
    search: str = Query(
        None,
        description="Từ khóa tìm kiếm theo tên đề tài"
    ),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_research_projects(
        db,
        current_user.id,
        search
    )


@router.get(
    "/{project_id}",
    response_model=ResearchProjectResponse,
    summary="Lấy đề tài nghiên cứu theo ID",
    description="Chỉ Owner hoặc Member của đề tài mới được xem thông tin."
)
def get_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_research_project_by_id(
        db,
        project_id,
        current_user.id
    )


@router.put(
    "/{project_id}",
    response_model=ResearchProjectResponse,
    summary="Cập nhật đề tài nghiên cứu",
    description="Chỉ Owner của đề tài mới được cập nhật."
)
def update_project(
    project_id: int,
    project: ResearchProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return update_research_project(
        db,
        project_id,
        current_user.id,
        project.name,
        project.description
    )


@router.delete(
    "/{project_id}",
    status_code=200,
    summary="Xóa đề tài nghiên cứu",
    description="Chỉ Owner của đề tài mới được xóa."
)
def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return delete_research_project(
        db,
        project_id,
        current_user.id
    )


@router.post(
    "/{project_id}/members",
    response_model=ResearchMemberResponse,
    status_code=201,
    summary="Thêm thành viên",
    description="Owner thêm một user vào đề tài nghiên cứu."
)
def add_member(
    project_id: int,
    member: ResearchMemberCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return add_research_member(
        db,
        project_id,
        current_user.id,
        member.user_id
    )


@router.delete(
    "/{project_id}/members/{user_id}",
    status_code=200,
    summary="Xóa thành viên",
    description="Owner xóa một thành viên khỏi đề tài nghiên cứu."
)
def delete_member(
    project_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return delete_research_member(
        db,
        project_id,
        current_user.id,
        user_id
    )


@router.get(
    "/{project_id}/members",
    response_model=list[ResearchMemberResponse],
    summary="Lấy danh sách thành viên",
    description="Lấy danh sách thành viên và role của từng thành viên trong đề tài."
)
def get_members(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_research_project_members(
        db,
        project_id,
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