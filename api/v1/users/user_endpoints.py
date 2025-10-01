from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession


from fastapi import APIRouter, Depends
from api.v1.depends import get_current_user, get_privy_id_from_token
from schemas.user_schemas import UserDetailSchema
from usecases.users.user_usecase import get_user_balance_usecase


router = APIRouter(prefix="/user", tags=["user"])


@router.get("/current_user")
async def get_current_user_by_access_token(
    user: str = Depends(get_current_user),
) -> UserDetailSchema:
        return await user



@router.get("/user/balance")
async def get_user_balance(
    privy_id: str = Depends(get_privy_id_from_token),
) -> dict:
        balance = await get_user_balance_usecase(privy_id=privy_id)
        return {"balance": balance}

