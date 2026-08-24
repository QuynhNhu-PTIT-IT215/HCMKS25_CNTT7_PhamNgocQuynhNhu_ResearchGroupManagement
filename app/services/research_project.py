from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.research_project import ResearchProject, ResearchMember


def create_research_project(db: Session,user_id: int,name: str,description: str):
    project = ResearchProject(
        name=name,
        description=description,
        owner_id=user_id
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    member = ResearchMember(
        project_id=project.id,
        user_id=user_id,
        role="Owner"
    )

    db.add(member)
    db.commit()
    db.refresh(member)

    return project


def get_research_projects(db: Session,user_id: int,search: str):
    query = db.query(ResearchProject).join(ResearchMember,ResearchMember.project_id == ResearchProject.id).filter(ResearchMember.user_id == user_id)

    if search:
        query = query.filter(ResearchProject.name.ilike(f"%{search}%"))

    return query.all()


def get_research_project_by_id(db: Session,project_id: int,user_id: int):
    if project_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="ID đề tài không hợp lệ"
        )

    project = db.query(ResearchProject).filter(ResearchProject.id == project_id).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy đề tài"
        )

    member = db.query(ResearchMember).filter(ResearchMember.project_id == project_id,ResearchMember.user_id == user_id).first()

    if not member:
        raise HTTPException(
            status_code=403,
            detail="Bạn không có quyền truy cập đề tài này"
        )

    return project