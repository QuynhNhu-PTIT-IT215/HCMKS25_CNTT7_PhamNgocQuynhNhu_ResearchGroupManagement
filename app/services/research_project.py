from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.research_project import ResearchProject, ResearchMember
from app.models.history import History


def create_research_project(db: Session,user_id: int,name: str,description: str):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy người dùng"
        )

    name = name.strip()

    if not name:
        raise HTTPException(
            status_code=400,
            detail="Tên đề tài không được để trống"
        )

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

    history = History(
        user_id=user_id,
        action="CREATE_PROJECT",
        project_id=project.id
    )

    db.add(history)
    db.commit()

    return project


def get_research_projects(db: Session,user_id: int,search: str):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy người dùng"
        )

    query = db.query(ResearchProject).join(ResearchMember,ResearchMember.project_id == ResearchProject.id).filter(
        ResearchMember.user_id == user_id
        )

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


def update_research_project(db: Session,project_id: int,user_id: int,name: str,description: str):
    project = db.query(ResearchProject).filter(ResearchProject.id == project_id).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy đề tài"
        )

    if project.owner_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Chỉ OWNER mới có quyền sửa đề tài"
        )

    name = name.strip()
    if not name:
        raise HTTPException(
            status_code=400,
            detail="Tên đề tài không được để trống"
        )

    project.name = name
    project.description = description

    history = History(
        user_id=user_id,
        action="UPDATE_PROJECT",
        project_id=project_id
    )

    db.add(history)
    db.commit()
    db.refresh(project)

    return project


def delete_research_project(db: Session,project_id: int,user_id: int):
    project = db.query(ResearchProject).filter(ResearchProject.id == project_id).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy đề tài"
        )

    if project.owner_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Chỉ OWNER mới có quyền xóa đề tài"
        )

    db.query(ResearchMember).filter(ResearchMember.project_id == project_id).delete()

    db.delete(project)
    db.commit()

    return {
        "message": "Xóa đề tài thành công"
    }


def add_research_member(db: Session,project_id: int,owner_id: int,user_id: int):
    project = db.query(ResearchProject).filter(ResearchProject.id == project_id).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy đề tài"
        )

    if project.owner_id != owner_id:
        raise HTTPException(
            status_code=403,
            detail="Chỉ OWNER mới có quyền thêm thành viên"
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy người dùng"
        )

    member = db.query(ResearchMember).filter(
        ResearchMember.project_id == project_id,
        ResearchMember.user_id == user_id
    ).first()

    if member:
        raise HTTPException(
            status_code=400,
            detail="Người dùng đã là thành viên của đề tài"
        )

    new_member = ResearchMember(
        project_id=project_id,
        user_id=user_id,
        role="Member"
    )

    db.add(new_member)

    history = History(
        user_id=owner_id,
        action="ADD_MEMBER",
        project_id=project_id,
        target_user_id=user_id
    )

    db.add(history)
    db.commit()
    db.refresh(new_member)

    return new_member


def delete_research_member(
    db: Session,
    project_id: int,
    owner_id: int,
    user_id: int
):
    project = db.query(ResearchProject).filter(
        ResearchProject.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy đề tài"
        )

    if project.owner_id != owner_id:
        raise HTTPException(
            status_code=403,
            detail="Chỉ OWNER mới có quyền xóa thành viên"
        )

    member = db.query(ResearchMember).filter(
        ResearchMember.project_id == project_id,
        ResearchMember.user_id == user_id
    ).first()

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Người dùng không phải thành viên của đề tài"
        )

    if member.role == "Owner":
        raise HTTPException(
            status_code=400,
            detail="Không thể xóa OWNER"
        )

    owner_count = db.query(ResearchMember).filter(
        ResearchMember.project_id == project_id,
        ResearchMember.role == "Owner"
    ).count()

    if member.role == "Owner" and owner_count <= 1:
        raise HTTPException(
            status_code=400,
            detail="Không thể xóa OWNER cuối cùng"
        )

    db.delete(member)

    history = History(
        user_id=owner_id,
        action="DELETE_MEMBER",
        project_id=project_id,
        target_user_id=user_id
    )

    db.add(history)
    db.commit()

    return {
        "message": "Xóa thành viên thành công"
    }


def get_research_project_members(
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
            detail="Không tìm thấy đề tài"
        )

    member = db.query(ResearchMember).filter(
        ResearchMember.project_id == project_id,
        ResearchMember.user_id == user_id
    ).first()

    if not member:
        raise HTTPException(
            status_code=403,
            detail="Bạn không có quyền xem thành viên của đề tài"
        )

    members = db.query(ResearchMember).filter(
        ResearchMember.project_id == project_id
    ).all()

    return members