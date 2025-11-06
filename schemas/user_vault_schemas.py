from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from schemas.enums import TransactionEnum


class UserVaultBase(BaseModel):
    transaction_method: Optional[TransactionEnum] = None
    amount: Optional[str] = None
    vault_address: Optional[str] = None


class UserVaultCreateRequest(UserVaultBase):
    transaction_method: Optional[TransactionEnum] = None


class UserVaultUpdateRequest(UserVaultBase):
    pass


class UserVaultCreateSchema(UserVaultBase):
    transaction_method: Optional[TransactionEnum] = None
    user_id: int


class UserVaultUpdateSchema(UserVaultBase):
    pass


class UserVaultResponseSchema(UserVaultBase):
    id: int
    user_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
