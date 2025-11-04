from sqlalchemy.ext.asyncio import AsyncSession

from engines.notification_engine import NotificationEngines
from schemas.notification_schemas import (
    SendNotificationRequest,
    SendNotificationResponse,
)


async def send_notification_usecase(
    user_id: int,
    payload: SendNotificationRequest,
    db_session: AsyncSession,
) -> SendNotificationResponse:
    notification_engine = NotificationEngines(db_session)
    result = await notification_engine.send_to_user(
        user_id=user_id,
        title=payload.title,
        body=payload.body,
        data=payload.data,
        priority=payload.priority.value.upper(),
        ttl=payload.ttl_seconds,
    )
    return SendNotificationResponse(**result)
