from typing import Any, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from core.constants import BASE_CHAIN, BASE_TRANSACTIONS_AVAILABLE_ASSETS, GET_BALANCE_ASSETS
from schemas.user_schemas import UserWalletsSchema, UserTransactionSchema 
from schemas.notification_schemas import CreateDeviceSchema
from typing import Iterable

from engines.user_engine import UserEngines
from engines.notification_engine import NotificationEngines
from core.config import get_app_settings
from core.integrations.privy_client import PrivyClient
from usecases.users.user_mapper import map_wallets
from usecases.users.user_mapper import mapResponseToUserCreateSchema


settings = get_app_settings()
privy_client = PrivyClient(settings)

async def check_user_usecase(privy_id: str, db_session: AsyncSession):
    user_engine = UserEngines(db_session)
    user = await user_engine.get_user_by_privy_id_or_none(privy_id=privy_id)

    if user == None:
        response = await privy_client.get_user_by_privy_id(privy_id=privy_id)
        user = await mapResponseToUserCreateSchema(response)
        return await user_engine.create_user(user=user)
    else:
        return user
    
  
async def get_user_balance_usecase(privy_id: str):
    wallet_ids = await get_user_wallet_ids(privy_id=privy_id)
    balance = await sum_wallets_usd(wallet_ids)

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
    result = await privy_client.list_wallets(privy_id=privy_id)
    wallets = map_wallets(result)
    return wallets
    

async def get_user_transactions_usecase(privy_user_id: str) -> List[UserTransactionSchema]: 
    wallet_ids = await get_user_wallet_ids(privy_user_id)

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
    

async def get_user_wallet_ids(privy_id:str):
    response = await privy_client.list_wallets(privy_id=privy_id)
    wallets = await extract_ids(response)
    return wallets

async def extract_ids(payload: Dict[str, Any]) -> List[str]:
    data = payload.get("data", [])
    return [item["id"] for item in data if isinstance(item, dict) and "id" in item]


async def sum_wallets_usd(wallet_ids: Iterable[str]):
    total = 0.0

    chains = BASE_CHAIN 
    assets = GET_BALANCE_ASSETS 

    for wid in wallet_ids:
        resp = await privy_client.get_wallet_balance(wallet_id=wid, asset=assets, chain=chains)

        for bal in resp.get("balances", []):
            usd_value = bal.get("display_values", {}).get("usd")
            if usd_value:
                total += float(usd_value)

    return total
