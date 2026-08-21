from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class UserBase(BaseModel):
    email: str
    full_name: str = Field(min_length=2, max_length=100)


class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=100)


class UserUpdate(BaseModel):
    email: str
    full_name: str = Field(min_length=2, max_length=100)
    password: str = Field(min_length=6, max_length=100)


class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)