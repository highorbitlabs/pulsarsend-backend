from sqlalchemy.ext.asyncio import AsyncSession

from engines.user_vault_engine import UserVaultEngines
from schemas.user_vault_schemas import (
    UserVaultCreateRequest,
    UserVaultCreateSchema,
    UserVaultUpdateRequest,
    UserVaultUpdateSchema,
)
from utils.exceptions.user_exceptions import UserVaultNotFoundException


async def create_user_vault_usecase(
    user_id: int,
    payload: UserVaultCreateRequest,
    db_session: AsyncSession,
):
    user_vault_engine = UserVaultEngines(db_session)
    data = UserVaultCreateSchema(
        user_id=user_id,
        **payload.model_dump(),
    )
    return await user_vault_engine.create_user_vault(payload=data)


async def get_user_vault_usecase(user_id: int, db_session: AsyncSession):
    user_vault_engine = UserVaultEngines(db_session)
    user_vault = await user_vault_engine.get_user_vault(user_id=user_id)
    if user_vault is None:
        raise UserVaultNotFoundException()
    return user_vault


async def update_user_vault_usecase(
    user_id: int,
    payload: UserVaultUpdateRequest,
    db_session: AsyncSession,
):
    user_vault_engine = UserVaultEngines(db_session)
    update_data = UserVaultUpdateSchema(
        **payload.model_dump(exclude_unset=True)
    )
    return await user_vault_engine.update_user_vault(
        user_id=user_id,
        payload=update_data,
    )
