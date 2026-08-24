from fastapi import APIRouter

from app.services.research_project import get_research_projects, get_research_project_by_id

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