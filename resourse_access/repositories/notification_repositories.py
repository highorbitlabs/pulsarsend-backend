from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from resourse_access.models.notification_models import DeviceDB
from sqlalchemy import select


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
                is_active=True
                )
            self.session.add(device)
            await self.session.commit()
        await self.session.flush()

        return device

    async def deactivate(self, user_id: int, token: str):
        self.model.query(DeviceDB).filter(DeviceDB.user_id==user_id, DeviceDB.fcm_token==token).update({"is_active": False})

    async def deactivate_many(self, tokens: List[str]):
        self.model.query(DeviceDB).filter(DeviceDB.fcm_token.in_(tokens)).update({"is_active": False}, synchronize_session=False)

    async def list_active_tokens(self, user_id: int) -> List[str]:
        return [t[0] for t in self.model.query(DeviceDB.fcm_token).filter(DeviceDB.user_id==user_id, DeviceDB.is_active==True)]
