from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from schemas.enums import NotificationPlatformEnum, NotificationPriorityEnum

class UnregisterBody(BaseModel):
    fcm_token: str

class CreateDeviceSchema(BaseModel):
    user_id: int
    fcm_token: str
    platform: NotificationPlatformEnum
    app_version: Optional[str] = None
    locale: Optional[str] = None
    is_active: Optional[bool] = None


class SendNotificationRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    body: str = Field(..., min_length=1, max_length=2000)
    data: Optional[Dict[str, Any]] = None
    priority: NotificationPriorityEnum = NotificationPriorityEnum.high
    ttl_seconds: int = Field(default=3600, ge=0)


class SendNotificationResponse(BaseModel):
    success: int
    failure: int
    deactivated: List[str]
