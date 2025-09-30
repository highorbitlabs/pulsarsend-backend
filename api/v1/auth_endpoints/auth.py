from __future__ import annotations


from fastapi import APIRouter, Depends

from api.v1.depends import get_privy_client
from core.integrations.privy import PrivyClient

from schemas.auth_schemas import TokenVerifyRequest
from schemas.auth_schemas import TokenVerifyResponse


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

