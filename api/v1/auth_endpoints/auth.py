from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession


from fastapi import APIRouter, Depends

from api.v1.depends import get_privy_client
from api.v1.depends import get_privy_id_from_token
from api.v1.depends import get_session

from core.integrations.privy import PrivyClient

from schemas.auth_schemas import TokenVerifyRequest
from schemas.auth_schemas import TokenVerifyResponse
from schemas.user_schemas import UserDetailSchema
from usecases.users.user_usecase import check_user_usecase


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token/verify", response_model=TokenVerifyResponse)
async def token_verify(
    payload: TokenVerifyRequest,
    privy_client: PrivyClient = Depends(get_privy_client),
) -> TokenVerifyResponse:
    result = await privy_client.token_verify(
        token=payload.token,
    )

    return TokenVerifyResponse.model_validate(result)


@router.post("/check/user")
async def check_user(
    privy_id: str = Depends(get_privy_id_from_token),
    db_session: AsyncSession = Depends(get_session),
) -> UserDetailSchema:
        return await check_user_usecase(privy_id=privy_id, db_session=db_session)

