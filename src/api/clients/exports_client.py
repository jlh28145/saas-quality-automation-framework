"""
Exports API client.
"""

from typing import Any, Dict
from src.api.clients.base_client import BaseClient
from src.utils.logger import get_logger

logger = get_logger("exports_client")


class ExportsClient(BaseClient):
    """Client for exports endpoints."""

    def request_export(self) -> Dict[str, Any]:
        """Request an export."""
        logger.info("Requesting export")
        response = self.post("/export", data={})
        return {
            "status_code": response.status_code,
            "body": response.json(),
            "response": response,
        }
