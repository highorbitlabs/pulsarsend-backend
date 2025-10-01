import base64
import requests
from sqlalchemy.ext.asyncio import AsyncSession

from engines.user_engine import UserEngines
from core.config import get_app_settings
from schemas.enums import UserRoleEnum
from schemas.user_schemas import UserCreateSchema


settings = get_app_settings()

async def check_user_usecase(privy_id: str, db_session: AsyncSession):
    user_engine = UserEngines(db_session)
    user = await user_engine.get_user_by_privy_id_or_none(privy_id=privy_id)

    if user == None:
        basic = base64.b64encode(f"{settings.PRIVY_APP_ID}:{settings.PRIVY_APP_SECRET}".encode()).decode()
        headers = {   #ToDo fix, use Builder Pattern
            "Authorization": f"Basic {basic}",
            "privy-app-id": settings.PRIVY_APP_ID  
        }

        response = requests.get(f"https://api.privy.io/v1/users/{privy_id}", headers=headers).json()
        user = await mapResponseToUserCreateSchema(response)
        return await user_engine.create_user(user=user)
    else:
        return user
    
  
# async def get_user_balance_usecase(privy_id: str):
#     basic = base64.b64encode(f"{settings.PRIVY_APP_ID}:{settings.PRIVY_APP_SECRET}".encode()).decode()
#     headers = {   #ToDo fix, use Builder Pattern
#         "Authorization": f"Basic {basic}",
#         "privy-app-id": settings.PRIVY_APP_ID  
#     }

#     response = requests.get("https://api.privy.io/v1/users", headers=headers).json()
#     user = await mapResponseToUserCreateSchema(response)
#     return await user_engine.create_user(user=user)



async def mapResponseToUserCreateSchema(data: dict):
    """Map Privy API user response -> UserCreateSchema""" #ToDo refactor like JavaMapper

    # Initialize fields
    email = None
    avatar_url = None

    for acc in data.get("linked_accounts", []):
        if acc.get("type") == "email" and not email:
            email = acc.get("address")
        elif acc.get("type") == "farcaster":
            avatar_url = acc.get("profile_picture_url") or acc.get("profile_picture")

    # Build schema object
    user = UserCreateSchema(
        privy_id=privy_id.split(":")[-1] if privy_id else None,  # strip did:privy:
        email=email,
        avatar_url=avatar_url,
        role=UserRoleEnum.user if hasattr(UserRoleEnum, "user") else None,
    )

    return user

        
        