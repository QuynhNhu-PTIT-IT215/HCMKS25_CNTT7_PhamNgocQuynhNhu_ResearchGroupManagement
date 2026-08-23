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
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ResearchMemberBase(BaseModel):
    project_id: int
    user_id: int
    role: str


class ResearchMemberCreate(ResearchMemberBase):
    pass


class ResearchMemberUpdate(BaseModel):
    role: str


class ResearchMemberResponse(ResearchMemberBase):
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)