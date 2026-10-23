import time
import requests
from typing import Optional, Dict
from backend.config import settings

class ShopifyAuthManager:
    def __init__(self):
        self._cached_token: Optional[str] = None
        self._expires_at: float = 0

    def get_access_token(self) -> str:
        # 1. If static admin token explicitly set in settings/env, use it
        if settings.admin_token and settings.admin_token.startswith("shpat_"):
            return settings.admin_token

        # 2. Check cached OAuth token
        now = time.time()
        if self._cached_token and self._expires_at > (now + 60):
            return self._cached_token

        # 3. Exchange client credentials with Shopify OAuth
        endpoint = f"https://{settings.shop}/admin/oauth/access_token"
        payload = {
            "client_id": settings.client_id,
            "client_secret": settings.client_secret,
            "grant_type": "client_credentials"
        }

        try:
            resp = requests.post(endpoint, data=payload, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            token = data.get("access_token")
            expires_in = data.get("expires_in", 86400)
            if not token:
                raise ValueError(f"No access_token returned from Shopify: {data}")

            self._cached_token = token
            self._expires_at = now + expires_in
            return token
        except Exception as e:
            # If OAuth fails, fallback to existing token if any
            if self._cached_token:
                return self._cached_token
            raise RuntimeError(f"Shopify OAuth exchange failed for {settings.shop}: {e}")

auth_manager = ShopifyAuthManager()
