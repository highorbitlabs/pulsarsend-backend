from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing import List

from fastapi import APIRouter, Depends
from api.v1.depends import get_current_user, get_privy_id_from_token
from schemas.user_schemas import UserDetailSchema
from usecases.users.user_usecase import get_user_balance_usecase
from usecases.users.user_usecase import get_user_wallets_usecase
from usecases.users.user_usecase import get_user_transactions_usecase

from schemas.user_schemas import UserWalletsSchema


router = APIRouter(prefix="/user", tags=["user"])


@router.get("/current_user")
async def get_current_user_by_access_token(
    user: str = Depends(get_current_user),
) -> UserDetailSchema:
        return user



@router.get("/balance")
async def get_user_balance(
    privy_id: str = Depends(get_privy_id_from_token),
):
        balance = await get_user_balance_usecase(privy_id=privy_id)
        return {"balance": balance}


@router.get("/wallets", status_code=status.HTTP_200_OK, response_model=List[UserWalletsSchema])
async def get_user_wallets(
        privy_id: str = Depends(get_privy_id_from_token),
):
        return await get_user_wallets_usecase(privy_id=privy_id)
        
@router.get("transactions", status_code=status.HTTP_200_OK) #response_model=UserWalletsSchema,
async def get_user_transactions(
        privy_id: str = Depends(get_privy_id_from_token),
):
        return await get_user_transactions_usecase(privy_user_id=privy_id)

