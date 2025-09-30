import asyncio
from typing import Any, Dict

from core.config import get_app_settings
from core.integrations.privy import PrivyClient
from utils.common_exceptions import PrivyApiException

import base64
from decimal import Decimal


import requests

APP_ID = 'cmfuyerug004yks0cpwvw02gk'
APP_SECRET = '2nbkxLYBwFRFnLr8awNL6EspBFJY16cKsb9mSsBwVGGm5d8XKeXC3kpA2EnuDinzVSmaQBsKJLNm1FPbdMekW46L'
WALLET_ID = 'rdtl5v4pkhtgtlcznanmactt'
ACCOUNT_ID = 'cmg0qj046001xjo0chf1rzg6x'

# clienta = PrivyAPI(
#     app_id="cmfuyerug004yks0cpwvw02gk",
#     app_secret="5ZUrNWgCPDhRs8FDgWjmoVuumveJvoYyjBJUbfcaUrsg9ZaVVfLWsfYEAJMEGFq6z7DBFxV3NViFeAZxKkm4A7Xa"
# )

# clienta.V


basic = base64.b64encode(f"{APP_ID}:{APP_SECRET}".encode()).decode()

resp = requests.get(
    f"https://api.privy.io/v1/wallets/{WALLET_ID}/balance",
    headers={
        "Authorization": f"Basic {basic}",
        "privy-app-id": APP_ID,
    },
    params={
        "chain": "ethereum",          
        "asset": "eth",          
        "include_currency": "usd" 
    },
    timeout=20,
)

resp.raise_for_status()
data = resp.json()
print(data)


headers = {
    "accept": "application/json",
    "privy-account-id": ACCOUNT_ID,
    "privy-app-id": APP_ID,
    "privy-app-secret": APP_SECRET,
}

def check_app():
    print("Start Check App")
    url = f"https://api.privy.io/api/v1/apps/{APP_ID}"
    resp = requests.get(url, headers=headers, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    print("App check OK:", data.get("name") or data.get("id"))

# check_app()

url = f"https://api.privy.io/v1/users/{ACCOUNT_ID}"

resp = requests.get(
    url,
    headers={
        "Authorization": f"Basic {basic}",
        "privy-app-id": APP_ID,
    },
    timeout=15
)

if resp.status_code == 200:
    print("✅ Connection OK. Account info:")
    print(resp.json())
else:
    print(f"❌ Failed. Status {resp.status_code}: {resp.text}")