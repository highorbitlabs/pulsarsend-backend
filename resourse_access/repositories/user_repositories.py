from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

from schemas.user_schemas import UserCreateSchema, UserDetailSchema
from utils.postgres_error_codes import FOREIGN_KEY_VIOLATION, UNIQUE_VIOLATION
from utils.exceptions.user_exceptions import DuplicateValueException, UserNotFoundException
from utils.exceptions.user_exceptions import RoleNotFoundException

from sqlalchemy.ext.asyncio import AsyncSession
from resourse_access.models.user_models import UserDB



class UserRepositories:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = UserDB
    
    async def create_user(self, user: UserCreateSchema):
        try:
            new_user = UserDB(**user.dict())
            self.session.add(new_user)
            await self.session.commit()
            await self.session.refresh(new_user)
            dto = UserDetailSchema.model_validate(new_user)
            return dto
        
        except IntegrityError as e:
            if e.orig.pgcode == UNIQUE_VIOLATION:
                raise DuplicateValueException()
            if e.orig.pgcode == FOREIGN_KEY_VIOLATION:
                raise RoleNotFoundException()


    async def get_user_by_privy_id(self, privy_id: str):
        try:
            query = await self.session.execute(
                select(self.model).where(self.model.privy_id == privy_id)
            )
            query_data = query.scalars().one()
            return query_data
        except NoResultFound:
            raise UserNotFoundException(message=f'User with privy_id: {privy_id} not found')
    
    async def get_user_by_privy_id_or_none(self, privy_id: str):
        """Return None if user not found"""
        query = await self.session.execute(
            select(self.model).where(self.model.privy_id == privy_id)
        )
        return query.scalars().one_or_none()