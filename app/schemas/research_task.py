from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ResearchTaskBase(BaseModel):
    title: str
    description: str
    assignee_id: int
    status: str
    priority: str
    due_date: datetime


class ResearchTaskCreate(BaseModel):
    title: str
    description: str
    assignee_id: int
    due_date: datetime
    priority: str


class ResearchTaskUpdate(BaseModel):
    title: str
    description: str
    assignee_id: int
    status: str
    priority: str
    due_date: datetime


class ResearchTaskResponse(ResearchTaskBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)