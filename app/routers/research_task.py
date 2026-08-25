from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.research_task import ResearchTaskUpdate

from app.services.research_task import (
    get_research_task_by_id,
    update_research_task,
    delete_research_task
)


router = APIRouter(
    prefix="/research-tasks",
    tags=["Research Tasks"]
)


@router.get("/{task_id}")
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


@router.patch("/{task_id}")
def update_task(
    task_id: int,
    task_data: ResearchTaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return update_research_task(
        db,
        task_id,
        current_user.id,
        task_data
    )


@router.delete("/{task_id}")
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