from fastapi import APIRouter, Depends

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
    get_research_task_by_id,
    create_research_task,
    get_research_tasks
)


router = APIRouter(
    prefix="/research-projects",
    tags=["Research Projects"]
)


@router.post(
    "",
    response_model=ResearchProjectResponse
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


@router.get("")
def get_projects(
    search: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_research_projects(
        db,
        current_user.id,
        search
    )


@router.get("/{project_id}")
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
    response_model=ResearchProjectResponse
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


@router.delete("/{project_id}")
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


@router.post("/{project_id}/members")
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


@router.delete("/{project_id}/members/{user_id}")
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
    response_model=list[ResearchMemberResponse]
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
    response_model=ResearchTaskResponse
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
    response_model=list[ResearchTaskResponse]
)
def get_tasks(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_research_tasks(
        db,
        project_id,
        current_user.id
    )