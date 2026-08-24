from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.research_task import ResearchTaskCreate, ResearchTaskResponse

from app.services.research_project import get_research_projects, get_research_project_by_id
from app.services.research_task import get_research_task_by_id, create_research_task


router = APIRouter(
    prefix="/research-projects",
    tags=["Research Projects"]
)


@router.get("")
def get_projects():
    return get_research_projects()


@router.get("/{project_id}")
def get_project(project_id: int):
    return get_research_project_by_id(project_id)

@router.post("/{project_id}/research-tasks", response_model= ResearchTaskResponse)
def create_task(
    project_id: int,
    task: ResearchTaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_research_task(db, project_id,current_user.id, task)