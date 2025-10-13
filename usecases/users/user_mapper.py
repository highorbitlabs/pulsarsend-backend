from typing import Any, Dict, List
from schemas.user_schemas import UserWalletsSchema

from schemas.enums import UserRoleEnum
from schemas.user_schemas import UserCreateSchema
from core.config import get_app_settings


settings = get_app_settings()

async def mapResponseToUserCreateSchema(data: dict) -> UserCreateSchema:

    privy_id = data.get("id")
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
        role=UserRoleEnum.user if hasattr(UserRoleEnum, "customer") else None,
    )

    return user

def map_wallets(payload: Dict[str, Any]) -> List[UserWalletsSchema]:
    wallets = []
    for item in payload.get("data", []) or []:
        wallets.append(UserWalletsSchema(
            wallet_id=item.get("id"),
            chain_type=item.get("chain_type"),
            policy_ids=item.get("policy_ids"),
            additional_signers=item.get("additional_signers"),
            created_at=item.get("created_at"),
            exported_at=item.get("exported_at"),
            imported_at=item.get("imported_at"),
        ))
    return wallets
        