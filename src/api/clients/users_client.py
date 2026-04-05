"""
Users API client.
"""

from typing import Any, Dict, List
from src.api.clients.base_client import BaseClient
from src.utils.logger import get_logger

logger = get_logger("users_client")


class UsersClient(BaseClient):
    """Client for users endpoints."""
    
    def list_users(self) -> Dict[str, Any]:
        """List all users."""
        logger.info("Fetching users list")
        response = self.get("/users")
        return {
            "status_code": response.status_code,
            "body": response.json(),
            "response": response,
        }
