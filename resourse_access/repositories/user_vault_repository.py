from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from resourse_access.models.user_models import UserVaultDB
from schemas.user_vault_schemas import (
    UserVaultCreateSchema,
    UserVaultUpdateSchema,
)
from utils.exceptions.user_exceptions import (
    UserVaultAlreadyExistsException,
    UserVaultNotFoundException,
)
from utils.postgres_error_codes import UNIQUE_VIOLATION


class UserVaultRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = UserVaultDB

    async def create(self, payload: UserVaultCreateSchema) -> UserVaultDB:
        user_vault = self.model(**payload.model_dump())
        self.session.add(user_vault)
        try:
            await self.session.commit()
        except IntegrityError as exc:
            await self.session.rollback()
            if getattr(exc.orig, "pgcode", None) == UNIQUE_VIOLATION:
                raise UserVaultAlreadyExistsException()
            raise
        await self.session.refresh(user_vault)
        return user_vault

    async def get_by_user_id(self, user_id: int) -> Optional[UserVaultDB]:
        query = await self.session.execute(
            select(self.model).where(self.model.user_id == user_id)
        )
        return query.scalars().one_or_none()

    async def update(self, user_id: int, payload: UserVaultUpdateSchema) -> UserVaultDB:
        user_vault = await self.get_by_user_id(user_id=user_id)
        if user_vault is None:
            raise UserVaultNotFoundException()

        data = payload.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(user_vault, field, value)

        try:
            await self.session.commit()
        except IntegrityError as exc:
            await self.session.rollback()
            if getattr(exc.orig, "pgcode", None) == UNIQUE_VIOLATION:
                raise UserVaultAlreadyExistsException()
            raise

        await self.session.refresh(user_vault)
        return user_vault
