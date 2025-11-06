from sqlalchemy.ext.asyncio import AsyncSession

from resourse_access.repositories.user_vault_repository import UserVaultRepository
from schemas.user_vault_schemas import (
    UserVaultCreateSchema,
    UserVaultUpdateSchema,
)


class UserVaultEngines:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user_vault(self, payload: UserVaultCreateSchema):
        repository = UserVaultRepository(self.session)
        return await repository.create(payload)

    async def get_user_vault(self, user_id: int):
        repository = UserVaultRepository(self.session)
        return await repository.get_by_user_id(user_id)

    async def update_user_vault(self, user_id: int, payload: UserVaultUpdateSchema):
        repository = UserVaultRepository(self.session)
        return await repository.update(user_id, payload)
