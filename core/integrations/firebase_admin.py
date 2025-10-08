import os
from pathlib import Path
import firebase_admin
from firebase_admin import credentials
from core.config import get_app_settings

settings = get_app_settings()

def init_firebase() -> None:
    # 1. Skip if Firebase disabled
    enabled = str(os.getenv("FIREBASE_ENABLED", "true")).lower() in ("1", "true", "yes")
    if not enabled:
        return

    # 2. Skip if already initialized
    if firebase_admin._apps:
        return

    # 3. Resolve credential path
    cred_path = settings.FIREBASE_CREDENTIALS_PATH
    if not cred_path:
        return

    path = Path(cred_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Firebase credential file not found: {path}")

    # 4. Initialize app
    cred = credentials.Certificate(str(path))
    firebase_admin.initialize_app(cred)
