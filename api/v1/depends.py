from fastapi import Security
from fastapi import HTTPException
from fastapi import Depends
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from jwt import PyJWKClient

from resourse_access.db_session import AsyncSessionLocal

from api.pagination import Pagination
from core.config import get_app_settings
from core.integrations.privy import PrivyClient


security = HTTPBearer()
settings = get_app_settings()
privy_client = PrivyClient(settings)
_jwk_client = PyJWKClient(settings.PRIVY_JWT_VERIFICATION_KEY_PEM)


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


async def get_pagination(offset: int = 0, limit: int = 20) -> Pagination:
    return Pagination(offset=offset, limit=limit)


async def get_privy_client() -> PrivyClient:
    return privy_client


async def get_payload_by_access_token(
        credentials: HTTPAuthorizationCredentials = Security(security)
) -> dict:
    """
    token payload = {"sub": user_id, "role": "backoffice", "exp": datetime, "scope": "access_token"}
    """
    current_access_token = credentials.credentials
    try:
        payload = jwt.decode(
            current_access_token, settings.ACCESS_TOKEN_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        if payload.get('scope') == 'access_token':
            return payload
        raise HTTPException(status_code=401, detail='Invalid scope for token')
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Access token expired')
    except jwt.JWTError as e:
        raise HTTPException(status_code=401, detail=str(e))

async def get_privy_id_from_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
    session=Depends(get_session),
) -> str:
    current_access_token = credentials.credentials
    try:
        signing_key = _jwk_client.get_signing_key_from_jwt(current_access_token).key
        
        payload = jwt.decode(
            current_access_token,
            signing_key,
            algorithms=[settings.ALGORITHM],
            audience=settings.PRIVY_APP_ID,  
            issuer="privy.io",
            options={"require": ["iss", "aud", "exp", "iat", "sub"]},
        )
        

        if payload.get("sub"):
            return payload.get("sub").split(":")[-1]
        raise HTTPException(status_code=401, detail='Access token expired')
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Access token expired')
    except jwt.JWTError as e:
        raise HTTPException(status_code=401, detail=str(e))
