"""
Forms API client.
"""

from typing import Any, Dict
from src.api.clients.base_client import BaseClient
from src.utils.logger import get_logger

logger = get_logger("forms_client")


class FormsClient(BaseClient):
    """Client for forms endpoints."""

    def submit_form(self, name: str, email: str, message: str) -> Dict[str, Any]:
        """Submit a form."""
        logger.info(f"Submitting form for: {name}")
        response = self.post(
            "/forms",
            data={
                "name": name,
                "email": email,
                "message": message,
            },
        )
        return {
            "status_code": response.status_code,
            "body": response.json(),
            "response": response,
        }
