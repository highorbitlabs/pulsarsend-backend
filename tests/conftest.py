import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Ensure the app boots with deterministic test configuration before imports resolve settings. 
#ToDo Fix it
os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("ACCESS_TOKEN_SECRET_KEY", "test-secret")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("PRIVY_APP_ID", "test-privy-app")
os.environ.setdefault("PRIVY_APP_SECRET", "test-privy-secret")
os.environ.setdefault("PRIVY_JWT_VERIFICATION_KEY_PEM", "https://example.com/jwks.json")
os.environ.setdefault("SUPABASE_ID", "test-supabase-id")
os.environ.setdefault("SUPABASE_KEY", "test-supabase-key")
os.environ.setdefault("SUPABASE_DB_CODE", "test-supabase-db-code")
os.environ.setdefault("FIREBASE_CREDENTIALS_PATH", "/tmp/firebase-test.json")
os.environ.setdefault("FIREBASE_ENABLED", "false")

from typing import Iterator

import pytest
from fastapi.testclient import TestClient

from core.config import get_app_settings
from main import app


@pytest.fixture(scope="session")
def test_client() -> Iterator[TestClient]:
    """
    Provide a FastAPI TestClient with a clean dependency override state per session.
    """
    # Clear any cached settings so the test-specific env vars above are honoured.
    get_app_settings.cache_clear()
    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True)
def _reset_dependency_overrides() -> Iterator[None]:
    """
    Keep dependency overrides isolated between tests.
    """
    app.dependency_overrides.clear()
    try:
        yield
    finally:
        app.dependency_overrides.clear()
