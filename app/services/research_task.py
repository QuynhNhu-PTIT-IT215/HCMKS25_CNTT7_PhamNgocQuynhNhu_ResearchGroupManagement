from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.research_task import ResearchTaskCreate, ResearchTaskUpdate
from app.models.research_project import ResearchProject, ResearchMember
from app.models.research_task import ResearchTask


def create_research_task(
    db: Session,
    project_id: int,
    user_id: int,
    task: ResearchTaskCreate
):
    project = db.query(ResearchProject).filter(
        ResearchProject.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy nhóm nghiên cứu"
        )

    member = db.query(ResearchMember).filter(
        ResearchMember.project_id == project_id,
        ResearchMember.user_id == user_id
    ).first()

    if not member:
        raise HTTPException(
            status_code=403,
            detail="Bạn không phải thành viên của đề tài"
        )

    if task.assignee_id is not None:
        assignee = db.query(ResearchMember).filter(
            ResearchMember.project_id == project_id,
            ResearchMember.user_id == task.assignee_id
        ).first()

        if not assignee:
            raise HTTPException(
                status_code=403,
                detail="Người được giao phải là thành viên của đề tài"
            )

    research_task = ResearchTask(
        project_id=project_id,
        title=task.title,
        description=task.description,
        assignee_id=task.assignee_id,
        due_date=task.due_date,
        priority=task.priority,
        status="TODO"
    )

    db.add(research_task)
    db.commit()
    db.refresh(research_task)

    return research_task


def get_research_tasks(
    db: Session,
    project_id: int,
    user_id: int
):
    project = db.query(ResearchProject).filter(
        ResearchProject.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy nhóm nghiên cứu"
        )

    member = db.query(ResearchMember).filter(
        ResearchMember.project_id == project_id,
        ResearchMember.user_id == user_id
    ).first()

    if not member:
        raise HTTPException(
            status_code=403,
            detail="Bạn không phải thành viên của đề tài"
        )

    return db.query(ResearchTask).filter(
        ResearchTask.project_id == project_id
    ).all()


def get_research_task_by_id(
    db: Session,
    task_id: int,
    user_id: int
):
    task = db.query(ResearchTask).filter(
        ResearchTask.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy nhiệm vụ nghiên cứu"
        )

    member = db.query(ResearchMember).filter(
        ResearchMember.project_id == task.project_id,
        ResearchMember.user_id == user_id
    ).first()

    if not member:
        raise HTTPException(
            status_code=403,
            detail="Bạn không thuộc đề tài nghiên cứu này"
        )

    return task


def update_research_task(
    db: Session,
    task_id: int,
    user_id: int,
    task_data: ResearchTaskUpdate
):
    task = db.query(ResearchTask).filter(
        ResearchTask.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy nhiệm vụ nghiên cứu"
        )

    member = db.query(ResearchMember).filter(
        ResearchMember.project_id == task.project_id,
        ResearchMember.user_id == user_id
    ).first()

    if not member:
        raise HTTPException(
            status_code=403,
            detail="Bạn không thuộc đề tài nghiên cứu này"
        )

    data = task_data.model_dump(exclude_unset=True)

    if "assignee_id" in data and data["assignee_id"] is not None:
        assignee = db.query(ResearchMember).filter(
            ResearchMember.project_id == task.project_id,
            ResearchMember.user_id == data["assignee_id"]
        ).first()

        if not assignee:
            raise HTTPException(
                status_code=403,
                detail="Người được giao phải là thành viên của đề tài"
            )

    for key, value in data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


def delete_research_task(
    db: Session,
    task_id: int,
    user_id: int
):
    task = db.query(ResearchTask).filter(
        ResearchTask.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy nhiệm vụ nghiên cứu"
        )

    project = db.query(ResearchProject).filter(
        ResearchProject.id == task.project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy đề tài nghiên cứu"
        )

    if project.owner_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Chỉ chủ đề tài mới có quyền xóa nhiệm vụ"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Xóa nhiệm vụ nghiên cứu thành công"
    }