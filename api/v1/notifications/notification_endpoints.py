from __future__ import annotations

from starlette import status

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.depends import get_current_user, get_session
from schemas.notification_schemas import (
    SendNotificationRequest,
    SendNotificationResponse,
)
from schemas.user_schemas import UserDetailSchema
from usecases.notifications.notification_usecase import send_notification_usecase

router = APIRouter(prefix="/notifications", tags=["notification"])


@router.post(
    "/send",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=SendNotificationResponse,
)
async def send_notification(
    payload: SendNotificationRequest,
    current_user: UserDetailSchema = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_session),
) -> SendNotificationResponse:
    user_id = getattr(current_user, "id", None)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current user is missing an id",
        )

    return await send_notification_usecase(
        user_id=user_id,
        payload=payload,
        db_session=db_session,
    )
