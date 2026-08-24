from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone

from app.db.database import Base


class History(Base):
    __tablename__ = "histories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    action = Column(String(50), nullable=False)
    project_id = Column(Integer, nullable=True)
    target_user_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    