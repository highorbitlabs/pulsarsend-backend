from __future__ import annotations

from typing import List
from starlette import status

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.depends import get_current_user, get_privy_id_from_token, get_session
from schemas.user_schemas import UserDetailSchema, UserWalletsSchema
from schemas.user_vault_schemas import (
    UserVaultCreateRequest,
    UserVaultResponseSchema,
    UserVaultUpdateRequest,
)

from usecases.users.user_usecase import (
    get_user_balance_usecase,
    get_user_transactions_usecase,
    get_user_wallets_usecase,
)
from usecases.users.user_vault_usecase import (
    create_user_vault_usecase,
    get_user_vault_usecase,
    update_user_vault_usecase,
)


router = APIRouter(prefix="/user", tags=["user"])


@router.get("/current_user", response_model=UserDetailSchema)
async def get_current_user_by_access_token(
    user: UserDetailSchema = Depends(get_current_user),
) -> UserDetailSchema:
    return user


@router.get("/balance")
async def get_user_balance(
    privy_id: str = Depends(get_privy_id_from_token),
) -> dict:
    balance = await get_user_balance_usecase(privy_id=privy_id)
    return {"balance": balance}


@router.get(
    "/wallets",
    status_code=status.HTTP_200_OK,
    response_model=List[UserWalletsSchema],
)
async def get_user_wallets(
    privy_id: str = Depends(get_privy_id_from_token),
) -> List[UserWalletsSchema]:
    return await get_user_wallets_usecase(privy_id=privy_id)


@router.get("/transactions", status_code=status.HTTP_200_OK)
async def get_user_transactions(
        privy_id: str = Depends(get_privy_id_from_token),
):
        # return await get_user_transactions_usecase(privy_user_id=privy_id)  #ToDo fix it
        return [
                {
                "caip2": "eip155:8453",
                "transaction_hash": "0x03fe1b0fd11a74d277a5b7a68b762de906503b82cbce2fc791250fd2b77cf137",
                "status": "confirmed",
                "created_at": 1746920539240,
                "privy_transaction_id": "au6wxoyhbw4yhwbn1s5v9gs9",
                "wallet_id": "xs76o3pi0v5syd62ui1wmijw",
                "details": {
                        "type": "transfer_sent",
                        "chain": "base",
                        "asset": "eth",
                        "sender": "0xa24c8d74c913e5dba36e45236c478f37c8bba20e",
                        "sender_privy_user_id": "rkiz0ivz254drv1xw982v3jq",
                        "recipient": "0x38bc05d7b69f63d05337829fa5dc4896f179b5fa",
                        "recipient_privy_user_id": "cmakymbpt000te63uaj85d9r6",
                        "raw_value": "1",
                        "raw_value_decimals": 18,
                        "display_values": {
                        "eth": "0.000000000000000001"
                        }
                }
                }
                ]


@router.post(
    "/vault",
    status_code=status.HTTP_201_CREATED,
    response_model=UserVaultResponseSchema,
)
async def create_user_vault(
    payload: UserVaultCreateRequest,
    current_user: UserDetailSchema = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_session),
) -> UserVaultResponseSchema:
    return await create_user_vault_usecase(
        user_id=current_user.id,
        payload=payload,
        db_session=db_session,
    )


@router.get(
    "/vault",
    status_code=status.HTTP_200_OK,
    response_model=UserVaultResponseSchema,
)
async def get_user_vault(
    current_user: UserDetailSchema = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_session),
) -> UserVaultResponseSchema:
    return await get_user_vault_usecase(
        user_id=current_user.id,
        db_session=db_session,
    )


@router.put(
    "/vault",
    status_code=status.HTTP_200_OK,
    response_model=UserVaultResponseSchema,
)
async def update_user_vault(
    payload: UserVaultUpdateRequest,
    current_user: UserDetailSchema = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_session),
) -> UserVaultResponseSchema:
    return await update_user_vault_usecase(
        user_id=current_user.id,
        payload=payload,
        db_session=db_session,
    )
