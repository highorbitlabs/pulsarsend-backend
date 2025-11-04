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
        self.registry.deactivate(user_id, token)
        self.db.commit()

    async def send_to_user(self, user_id: int, title: str, body: str,
                     data: Optional[Dict[str, Any]] = None, priority: str = "HIGH", ttl: int = 3600):
        tokens = self.registry.list_active_tokens(user_id)
        results = self.sender.send_to_tokens(tokens, title, body, data or {}, priority, ttl)
        deactivated = [t for (t, ok, code) in results if not ok and code == "UNREGISTERED"]
        if deactivated:
            self.registry.deactivate_many(deactivated)
        self.db.commit()
        return {
            "success": sum(1 for _, ok, _ in results if ok),
            "failure": sum(1 for _, ok, _ in results if not ok),
            "deactivated": deactivated,
        }
