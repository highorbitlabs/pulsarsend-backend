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

    model_config = ConfigDict(from_attributes=True)


class UserCreateSchema(BaseModel):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    privy_id: Optional[str] = None
    email: Optional[str] = None
    role: Optional[UserRoleEnum] = None
    phone_number: Optional[str] = None
    gender: Optional[GenderEnum] = None
    avatar_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UserWalletsSchema(BaseModel):
    wallet_id: Optional[str]
    chain_type: Optional[str] = None
    policy_ids: Optional[list] = None
    additional_signers: Optional[list] = None
    created_at: Optional[int] = None
    exported_at: Optional[int] = None
    imported_at: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
