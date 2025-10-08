import base64
from typing import Any, Dict, List
import requests
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from core.constants import BASE_CHAIN, BASE_TRANSACTIONS_AVAILABLE_ASSETS
from schemas.user_schemas import UserWalletsSchema
from schemas.notification_schemas import CreateDeviceSchema


from engines.user_engine import UserEngines
from engines.notification_engine import NotificationEngines
from core.config import get_app_settings
from schemas.enums import UserRoleEnum
from schemas.user_schemas import UserCreateSchema
from core.integrations.privy_client import PrivyClient


settings = get_app_settings()
privy_client = PrivyClient(settings)

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
    
  
async def get_user_balance_usecase(privy_id: str):
    wallets = await get_user_wallets_list(privy_id=privy_id)
    balance = await sum_wallets_usd(wallets)

    return balance
  
async def create_user_device_usecase(device: CreateDeviceSchema, db_session: AsyncSession):
    notification_engine = NotificationEngines(db_session)
    device = await notification_engine.register_token(
        user_id=device.user_id,
        fcm_token=device.fcm_token,
        platform=device.platform,
        app_version=device.app_version,
        locale=device.locale
        )
    return device


async def get_user_wallets_usecase(privy_id: str) -> List[UserWalletsSchema]:
    result = await privy_client.list_wallets(user_id=privy_id)
    wallets = map_wallets(result)
    return wallets
    

async def get_user_transactions_usecase(privy_user_id: str) -> List[Dict[str, Any]]:
    wallet_ids = await get_user_wallets_list(privy_user_id)

    tasks = [
        privy_client.get_transactions(
            wallet_id=wid,
            chain=BASE_CHAIN,
            asset=BASE_TRANSACTIONS_AVAILABLE_ASSETS
        )
        for wid in wallet_ids
    ]

    # Run all requests in parallel
    results = await asyncio.gather(*tasks)

    # Collect all transactions from results
    all_transactions: List[Dict[str, Any]] = []
    for result in results:
        transactions = result.get("transactions", []) or []
        all_transactions.extend(transactions)

    # Sort by creation time (newest first)
    all_transactions.sort(
        key=lambda tx: int(tx.get("created_at", 0)),
        reverse=True
    )

    return all_transactions
    

async def get_user_wallets_list(privy_id:str):
    url = "https://api.privy.io/v1/wallets"
    basic = base64.b64encode(f"{settings.PRIVY_APP_ID}:{settings.PRIVY_APP_SECRET}".encode()).decode()


    response = requests.get(
        url,
        headers={
            "Authorization": f"Basic {basic}",
            "privy-app-id": settings.PRIVY_APP_ID,
        },
        params={"user_id": privy_id},
        timeout=15
    )
    wallets = await extract_ids(response.json())
    return wallets

async def extract_ids(payload: Dict[str, Any]) -> List[str]:

    data = payload.get("data", [])
    return [item["id"] for item in data if isinstance(item, dict) and "id" in item]

import base64, requests
from typing import Iterable

async def sum_wallets_usd(wallet_ids: Iterable[str]):
    total = 0.0
    basic = base64.b64encode(
        f"{settings.PRIVY_APP_ID}:{settings.PRIVY_APP_SECRET}".encode()
    ).decode()

    headers = {
        "Authorization": f"Basic {basic}",
        "privy-app-id": settings.PRIVY_APP_ID,
    }

    # repeat params as tuples
    chains = ["ethereum"] # "base", "polygon", "solana"
    assets = ["eth", "usdc", "usdt"] 

    for wid in wallet_ids:
        url = f"https://api.privy.io/v1/wallets/{wid}/balance"

        params = [("include_currency", "usd")]
        params += [("chain", c) for c in chains]
        params += [("asset", a) for a in assets]

        resp = requests.get(url, headers=headers, params=params, timeout=15)
        resp.raise_for_status()

        data = resp.json()
        for bal in data.get("balances", []):
            usd_value = bal.get("display_values", {}).get("usd")
            if usd_value:
                total += float(usd_value)

    return total


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
        