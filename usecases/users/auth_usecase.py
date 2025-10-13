from core.config import get_app_settings
from core.integrations.privy_client import PrivyClient
from schemas.auth_schemas import TokenVerifyResponse 


settings = get_app_settings()
privy_client = PrivyClient(settings)

async def token_verify_usecase(token: str) -> TokenVerifyResponse:
    request = await privy_client.token_verify(token=token)
    return request
