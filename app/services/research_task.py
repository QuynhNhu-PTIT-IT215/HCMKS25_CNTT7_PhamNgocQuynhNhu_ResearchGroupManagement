from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.research_task import ResearchTaskCreate 
from app.models.research_project import ResearchProject, ResearchMember

def create_research_task(db: Session,project_id: int,user_id: int,task: ResearchTaskCreate):
    project = db.query(ResearchProject).filter(ResearchProject.id == project_id).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy nhóm nghiên cứu"
        )


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