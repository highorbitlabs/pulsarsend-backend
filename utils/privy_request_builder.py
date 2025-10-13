from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class PrivyRequest:
    method: str
    url: str
    headers: Dict[str, str]
    json: Optional[Dict[str, Any]]
    params: Optional[Dict[str, Any]]
    timeout: float

class PrivyRequestBuilder:
    def __init__(self, base_url: str, headers: Dict[str, str], timeout: float) -> None:
        self._base_url = base_url.rstrip("/")
        self._headers = headers
        self._timeout = timeout
        self._method = "GET"
        self._path = ""
        self._json = None
        self._params = None

    def with_method(self, method: str) -> "PrivyRequestBuilder":
        self._method = method.upper()
        return self

    def with_path(self, path: str) -> "PrivyRequestBuilder":
        self._path = path.lstrip("/")
        return self

    def with_json(self, payload: Dict[str, Any]) -> "PrivyRequestBuilder":
        self._json = payload
        return self

    def with_params(self, params: Dict[str, Any]) -> "PrivyRequestBuilder":
        self._params = params
        return self

    def build(self) -> PrivyRequest:
        return PrivyRequest(
            method=self._method,
            url=f"{self._base_url}/{self._path}",
            headers=self._headers,
            json=self._json,
            params=self._params,
            timeout=self._timeout,
        )
    