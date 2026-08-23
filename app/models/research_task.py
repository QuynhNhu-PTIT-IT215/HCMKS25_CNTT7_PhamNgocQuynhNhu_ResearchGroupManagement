from app.db.database import Base
from sqlalchemy import Column,String, Integer, Text, ForeignKey, DateTime, Enum
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

class ResearchTask(Base):
    __tablename__ = 'research_tasks'

    id = Column(Integer, primary_key=True)

    project_id = Column(ForeignKey('research_projects.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    assignee_id = Column(ForeignKey('users.id'), nullable=True)
    status = Column(Enum('TODO', 'IN_PROGRESS', 'DONE'))
    priority = Column(Enum('LOW', 'MEDIUM', 'HIGH'))
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    project = relationship('ResearchProject', back_populates='research_tasks')
    assignee = relationship('User', back_populates='assigned_tasks')