from fastapi import APIRouter

from app.services.research_task import (
    get_research_task_by_id
)


router = APIRouter(
    prefix="/research-tasks",
    tags=["Research Tasks"]
)


@router.get("/{task_id}")
def get_task(task_id: int):
    return get_research_task_by_id(task_id)