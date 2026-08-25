from pydantic import BaseModel, ConfigDict, field_validator
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

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, value):
        if value not in ["LOW", "MEDIUM", "HIGH"]:
            raise ValueError("Priority phải là LOW, MEDIUM hoặc HIGH")
        return value


class ResearchTaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    assignee_id: int | None = None
    status: str | None = None
    priority: str | None = None
    due_date: datetime | None = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        if value not in ["TODO", "IN_PROGRESS", "DONE"]:
            raise ValueError("Status phải là TODO, IN_PROGRESS hoặc DONE")
        return value

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, value):
        if value not in ["LOW", "MEDIUM", "HIGH"]:
            raise ValueError("Priority phải là LOW, MEDIUM hoặc HIGH")
        return value


class ResearchTaskResponse(ResearchTaskBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)