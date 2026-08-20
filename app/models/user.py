from app.db.database import Base
from sqlalchemy import Column, Integer, Enum, String, Boolean, DateTime
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(Enum('User', 'Admin'), default='User')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default= datetime.now(timezone.utc))

    memberships = relationship('ResearchMember', back_populates='user')
    assigned_tasks = relationship('ResearchTask', back_populates='assignee')
    owned_projects = relationship('ResearchProject', back_populates='owner')