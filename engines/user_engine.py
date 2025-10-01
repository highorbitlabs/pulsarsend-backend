from sqlalchemy.ext.asyncio import AsyncSession
from resourse_access.repositories.user_repositories import UserRepositories
from schemas.user_schemas import UserCreateSchema, UserDetailSchema

class UserEngines:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def check_user(self, privy_id):
        repository = UserRepositories(session=self.session)
        return await repository.create_user(privy_id=privy_id)

    async def create_user(self, user: UserCreateSchema):
        repository = UserRepositories(session=self.session)
        return await repository.create_user(user=user)


    async def get_user_by_privy_id(self, privy_id: str):
        repository = UserRepositories(session=self.session)
        return await repository.get_user_by_privy_id(privy_id=privy_id)


    async def get_user_by_privy_id_or_none(self, privy_id: str):
        repository = UserRepositories(session=self.session)
        return await repository.get_user_by_privy_id_or_none(privy_id=privy_id)


