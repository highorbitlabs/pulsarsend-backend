from typing import Dict, Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from resourse_access.repositories.notification_repositories import DeviceRegistry
from utils.fcm_sender import FcmNotificationSender

class NotificationEngines:
    def __init__(self, db: AsyncSession):
        self.registry = DeviceRegistry(db)
        self.sender = FcmNotificationSender()
        self.db = db

    async def register_token(self, user_id: int, fcm_token: str, platform: str, app_version: Optional[str], locale: Optional[str]):
        device = await self.registry.upsert(user_id, fcm_token, platform, app_version, locale)
        await self.db.commit()
        await self.db.refresh(device)
        return device

    async def unregister_token(self, user_id: int, token: str):
        await self.registry.deactivate(user_id, token)
        await self.db.commit()

    async def send_to_user(self, user_id: int, title: str, body: str,
                     data: Optional[Dict[str, Any]] = None, priority: str = "HIGH", ttl: int = 3600):
        tokens = await self.registry.list_active_tokens(user_id)
        if not tokens:
            return {"success": 0, "failure": 0, "deactivated": []}

        normalized_priority = priority.upper()
        results = self.sender.send_to_tokens(tokens, title, body, data or {}, normalized_priority, ttl)
        deactivated = [t for (t, ok, code) in results if not ok and code == "UNREGISTERED"]
        if deactivated:
            await self.registry.deactivate_many(deactivated)
            await self.db.commit()
        return {
            "success": sum(1 for _, ok, _ in results if ok),
            "failure": sum(1 for _, ok, _ in results if not ok),
            "deactivated": deactivated,
        }
