from pydantic import BaseModel
from typing import Optional, Dict, Any

from schemas.enums import NotificationPlatformEnum


class RegisterBody(BaseModel):
    fcm_token: str
    platform: str
    app_version: Optional[str] = None
    locale: Optional[str] = None

class UnregisterBody(BaseModel):
    fcm_token: str

class SendBody(BaseModel):
    user_id: int
    title: str
    body: str
    data: Optional[Dict[str, Any]] = None
    priority: Optional[str] = "HIGH"
    ttl_seconds: Optional[int] = 3600

class CreateDeviceSchema(BaseModel):
    user_id: int
    fcm_token: str
    platform: NotificationPlatformEnum
    app_version: Optional[str] = None
    locale: Optional[str] = None
    is_active: Optional[bool] = None
