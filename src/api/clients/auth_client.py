"""
Authentication API client.
"""

from typing import Any, Dict, Optional
from src.api.clients.base_client import BaseClient
from src.utils.logger import get_logger

logger = get_logger("auth_client")


class AuthClient(BaseClient):
    """Client for authentication endpoints."""

    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Login with email and password."""
        logger.info(f"API login with email: {email}")
        response = self.post("/auth/login", data={"email": email, "password": password})
        return {
            "status_code": response.status_code,
            "body": response.json(),
            "response": response,
        }

    def get_token(self, email: str, password: str) -> Optional[str]:
        """Login and extract token."""
        result = self.login(email, password)
        if result["status_code"] == 200:
            return result["body"].get("token")
        return None
