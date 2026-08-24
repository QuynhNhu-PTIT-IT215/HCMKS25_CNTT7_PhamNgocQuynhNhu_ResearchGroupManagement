from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class ResearchProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str


class ResearchProjectCreate(ResearchProjectBase):
    pass


class ResearchProjectUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
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


class ResearchMemberCreate(BaseModel):
    user_id: int


class ResearchMemberUpdate(BaseModel):
    role: str


class ResearchMemberResponse(ResearchMemberBase):
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)