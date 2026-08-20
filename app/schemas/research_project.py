from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ResearchProjectBase(BaseModel):
    name: str
    description: str

class ResearchProjectCreate(ResearchProjectBase):
    pass

class ResearchProjectUpdate(BaseModel):
    name: str
    description: str

class ResearchProjectResponse(ResearchProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ResearchMemberBase(BaseModel):
    user_id: int
    project_id: int
    role: str

class ResearchMemberCreate(ResearchMemberBase):
    pass

class ResearchMemberUpdate(BaseModel):
    role: str

class ResearchMemberResponse(ResearchMemberBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)