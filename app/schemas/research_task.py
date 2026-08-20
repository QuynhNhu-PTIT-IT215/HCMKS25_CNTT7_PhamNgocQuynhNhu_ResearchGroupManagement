from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ResearchTaskBase(BaseModel):
    project_id: int
    title: str
    description: str
    status: str


class ResearchTaskCreate(ResearchTaskBase):
    pass

class ResearchTaskUpdate(BaseModel):
    title: str
    description: str
    status: str

class ResearchTaskResponse(ResearchTaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)