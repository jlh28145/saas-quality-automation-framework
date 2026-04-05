"""
Base HTTP client for API testing.
"""

from typing import Any, Dict, Optional
import requests
from src.utils.logger import get_logger

logger = get_logger("api_client")


class BaseClient:
    """Base class for API clients."""
    
    def __init__(self, base_url: str = "http://localhost:5000/api"):
        """Initialize client."""
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {"Content-Type": "application/json"}
    
    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> requests.Response:
        """Make HTTP request."""
        url = f"{self.base_url}{endpoint}"
        request_headers = {**self.headers}
        if headers:
            request_headers.update(headers)
        
        logger.debug(f"{method} {url}")
        
        response = self.session.request(
            method,
            url,
            json=data,
            headers=request_headers,
            **kwargs
        )
        
        logger.debug(f"Response status: {response.status_code}")
        return response
    
    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """GET request."""
        return self._request("GET", endpoint, **kwargs)
    
    def post(self, endpoint: str, data: Dict[str, Any] = None, **kwargs) -> requests.Response:
        """POST request."""
        return self._request("POST", endpoint, data=data, **kwargs)
    
    def put(self, endpoint: str, data: Dict[str, Any] = None, **kwargs) -> requests.Response:
        """PUT request."""
        return self._request("PUT", endpoint, data=data, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """DELETE request."""
        return self._request("DELETE", endpoint, **kwargs)
    
    def close(self) -> None:
        """Close session."""
        self.session.close()
