from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession


from fastapi import APIRouter, Depends

from api.v1.depends import get_privy_client
from api.v1.depends import get_privy_id_from_token
from api.v1.depends import get_session
from api.v1.depends import require_bearer_token

from core.integrations.privy_client import PrivyClient

from schemas.auth_schemas import TokenVerifyRequest
from schemas.auth_schemas import TokenVerifyResponse
from schemas.user_schemas import UserDetailSchema
from schemas.notification_schemas import CreateDeviceSchema
from usecases.users.user_usecase import check_user_usecase
from usecases.users.user_usecase import create_user_device_usecase
from usecases.users.auth_usecase import token_verify_usecase


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token/verify", response_model=TokenVerifyResponse)
async def token_verify(
    payload: TokenVerifyRequest
) -> TokenVerifyResponse:
    result = await token_verify_usecase(token=payload.token)
    return result


@router.post("/check/user")
async def check_user(
    privy_id: str = Depends(get_privy_id_from_token),
    db_session: AsyncSession = Depends(get_session),
) -> UserDetailSchema:
        return await check_user_usecase(privy_id=privy_id, db_session=db_session)


@router.post("/user/device")
async def create_user_device(
    device: CreateDeviceSchema,   
    db_session: AsyncSession = Depends(get_session),
    token: str = Depends(require_bearer_token)
):
    return await create_user_device_usecase(device=device, db_session=db_session)

