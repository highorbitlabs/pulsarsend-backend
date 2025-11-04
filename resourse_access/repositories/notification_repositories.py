from typing import List, Optional
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from resourse_access.models.notification_models import DeviceDB


class DeviceRegistry:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = DeviceDB
    

    async def upsert(self, user_id: int, fcm_token: str, platform: str, app_version: Optional[str], locale: Optional[str]):
        query = await self.session.execute(
            select(self.model).where(self.model.fcm_token == fcm_token)
        )
        device = query.scalar_one_or_none()
        if device:
            device.user_id = user_id
            device.platform = platform
            device.app_version = app_version
            device.locale = locale
            device.is_active = True
        else:
            device = DeviceDB(
                user_id=user_id,
                fcm_token=fcm_token,
                platform=platform,
                app_version=app_version,
                locale=locale,
                is_active=True,
            )
            self.session.add(device)
        await self.session.flush()

        return device

    async def deactivate(self, user_id: int, token: str):
        await self.session.execute(
            update(self.model)
            .where(self.model.user_id == user_id, self.model.fcm_token == token)
            .values(is_active=False)
        )

    async def deactivate_many(self, tokens: List[str]):
        if not tokens:
            return
        await self.session.execute(
            update(self.model)
            .where(self.model.fcm_token.in_(tokens))
            .values(is_active=False)
        )

    async def list_active_tokens(self, user_id: int) -> List[str]:
        query = await self.session.execute(
            select(self.model.fcm_token).where(
                self.model.user_id == user_id,
                self.model.is_active.is_(True),
            )
        )
        return [row[0] for row in query.all()]
