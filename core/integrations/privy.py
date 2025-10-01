from __future__ import annotations

from typing import Any, Dict, Optional, TYPE_CHECKING

import httpx

from utils.common_exceptions import PrivyApiException
from core.config import get_app_settings

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from jwt import PyJWKClient

if TYPE_CHECKING:
    from core.settings.app import AppSettings



class PrivyClient:
    def __init__(self, settings: AppSettings) -> None:
        self._base_url = str(settings.PRIVY_API_BASE_URL).rstrip("/")
        self._timeout = settings.PRIVY_API_TIMEOUT_SECONDS
        self._app_id = settings.PRIVY_APP_ID
        self._headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "privy-app-id": settings.PRIVY_APP_ID,
            "privy-app-secret": settings.PRIVY_APP_SECRET,
        }
        self._jwks_client = PyJWKClient(settings.PRIVY_JWT_VERIFICATION_KEY_PEM)


    async def token_verify(
        self,
        *,
        token: str,
    ) -> Dict[str, Any]:
        settings = get_app_settings()
        header = jwt.get_unverified_header(token)
        alg = header.get("alg")
        if alg not in ("ES256", "EdDSA"):
            raise ValueError(f"Unexpected alg: {alg}")

        signing_key = self._jwks_client.get_signing_key_from_jwt(token)

        claims = jwt.decode(
            token,
            key=signing_key.key,
            algorithms=[alg],
            audience=settings.PRIVY_APP_ID,
            issuer="privy.io",
            options={"require": ["iss", "aud", "exp", "iat", "sub"]},
        )

        return claims


    async def get_app_config(self) -> Dict[str, Any]:
        return await self._get(f"/api/v1/apps/{self._app_id}")

    async def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self._request("POST", path, payload)

    async def _get(self, path: str) -> Dict[str, Any]:
        return await self._request("GET", path)
    
    async def load_public_key(self, pem: str):
        return serialization.load_pem_public_key(pem.encode(), backend=default_backend())

    async def _request(
        self,
        method: str,
        path: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient(base_url=self._base_url, timeout=self._timeout) as client:
                response = await client.request(
                    method,
                    path,
                    json=payload,
                    headers=self._headers,
                )
        except httpx.RequestError as exc:
            raise PrivyApiException(message="Unable to reach Privy API", dev_message=str(exc)) from exc

        try:
            data = response.json()
        except ValueError:
            data = {"raw_response": response.text}

        if response.is_success:
            return data

        message = self._extract_error_message(data)
        dev_message = response.text if isinstance(data, dict) else str(data)
        raise PrivyApiException(message=message, code=response.status_code, dev_message=dev_message)

    @staticmethod
    def _extract_error_message(data: Dict[str, Any]) -> str:
        if isinstance(data, dict):
            for key in ("error", "message", "detail"):
                value = data.get(key)
                if isinstance(value, str) and value:
                    return value
        return "Privy API request failed"
