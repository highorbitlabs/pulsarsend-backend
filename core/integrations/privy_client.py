import base64
from typing import Any, Dict, Optional, Sequence, Union

import httpx

from core.integrations.privy import PrivyRequestBuilder
from core.integrations.privy import PrivyRequest
from core.settings.app import AppSettings
from utils.common_exceptions import PrivyApiException


class PrivyClient:
    def __init__(self, settings: AppSettings) -> None:
        self._base_url = str(settings.PRIVY_API_BASE_URL).rstrip("/")
        self._timeout = settings.PRIVY_API_TIMEOUT_SECONDS

        credentials = f"{settings.PRIVY_APP_ID}:{settings.PRIVY_APP_SECRET}".encode()
        basic_token = base64.b64encode(credentials).decode()

        self._headers = {
            "Authorization": f"Basic {basic_token}",
            "privy-app-id": settings.PRIVY_APP_ID,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    async def token_verify(self, *, token: str) -> Dict[str, Any]:
        request = (
            PrivyRequestBuilder(self._base_url, self._headers, self._timeout)
            .with_method("POST")
            .with_path("auth/token/verify")
            .with_json({"token": token})
            .build()
        )

        return await self._send(request)

    async def list_wallets(
        self,
        *,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        chain_type: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {}

        if cursor is not None:
            params["cursor"] = cursor
        if limit is not None:
            if limit > 100:
                raise ValueError("Privy limit must be <= 100")
            params["limit"] = limit
        if chain_type is not None:
            params["chain_type"] = chain_type
        if user_id is not None:
            params["user_id"] = user_id

        builder = (
            PrivyRequestBuilder(self._base_url, self._headers, self._timeout)
            .with_method("GET")
            .with_path("v1/wallets")
        )

        if params:
            builder = builder.with_params(params)

        request = builder.build()

        return await self._send(request)

    async def get_transactions(
        self,
        *,
        wallet_id: str,
        chain: str,
        asset: Union[str, Sequence[str]],
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        if not wallet_id:
            raise ValueError("wallet_id is required")
        if not chain:
            raise ValueError("chain is required")
        if asset is None:
            raise ValueError("asset is required")
        if limit is not None and limit > 100:
            raise ValueError("Privy limit must be <= 100")

        params: Dict[str, Any] = {"chain": chain}

        if cursor is not None:
            params["cursor"] = cursor
        if limit is not None:
            params["limit"] = limit

        if isinstance(asset, str):
            if not asset:
                raise ValueError("asset must not be empty")
            params["asset"] = asset
        else:
            asset_list = [value for value in asset if value]
            if any(not isinstance(value, str) for value in asset_list):
                raise ValueError("asset values must be strings")
            if not asset_list:
                raise ValueError("asset must contain at least one value")
            if len(asset_list) > 2:
                raise ValueError("Privy supports at most 2 assets per request")
            params["asset"] = asset_list

        builder = (
            PrivyRequestBuilder(self._base_url, self._headers, self._timeout)
            .with_method("GET")
            .with_path(f"v1/wallets/{wallet_id}/transactions")
            .with_params(params)
        )

        request = builder.build()

        return await self._send(request)

    async def _send(self, request: PrivyRequest) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=request.timeout) as client:
                response = await client.request(
                    method=request.method,
                    url=request.url,
                    headers=request.headers,
                    json=request.json,
                    params=request.params,
                )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise PrivyApiException(
                message="Privy API request failed",
                code=exc.response.status_code,
                dev_message=exc.response.text,
            ) from exc
        except httpx.HTTPError as exc:
            raise PrivyApiException(dev_message=str(exc)) from exc

        return response.json()
