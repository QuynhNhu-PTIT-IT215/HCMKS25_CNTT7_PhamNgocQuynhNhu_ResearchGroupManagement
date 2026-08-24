from app.db.database import Base
from sqlalchemy import Column,String, Integer, Text, ForeignKey, DateTime, Enum
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

class ResearchProject(Base):
    __tablename__ = 'research_projects'

    id = Column(Integer, primary_key=True, autoincrement=True,index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    owner = relationship('User', back_populates='owned_projects')
    research_members = relationship('ResearchMember', back_populates='project')
    research_tasks = relationship('ResearchTask', back_populates='project')

class ResearchMember(Base):
    __tablename__ = 'research_members'

    project_id = Column(ForeignKey('research_projects.id'), primary_key=True)
    user_id = Column(ForeignKey('users.id'), nullable=False, primary_key=True)
    role = Column(Enum('Owner', 'Member'), nullable=False)
    joined_at = Column(DateTime, default= datetime.now(timezone.utc))

    user = relationship('User', back_populates='memberships')
    project = relationship('ResearchProject', back_populates='research_members')
