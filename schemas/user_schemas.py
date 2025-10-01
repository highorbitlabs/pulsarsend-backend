from datetime import datetime
from typing import Optional
from typing import Union

from pydantic import BaseModel, ConfigDict

from schemas.enums import GenderEnum, UserRoleEnum


class UserDetailSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    privy_id: Optional[str] = None
    email: Optional[str] = None
    role: Optional[UserRoleEnum] = None
    phone_number: Optional[str] = None
    gender: Optional[GenderEnum] = None
    avatar_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CurrentUser(BaseModel):
    id: int
    privy_id: str

    class Config:
        orm_mode = True


class UserCreateSchema(BaseModel):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    privy_id: Optional[str] = None
    email: Optional[str] = None
    role: Optional[UserRoleEnum] = None
    phone_number: Optional[str] = None
    gender: Optional[GenderEnum] = None
    avatar_url: Optional[str] = None

    class Config:
        orm_mode = True
