"""
JSON Schema validation assertions.
"""

from typing import Any, Dict
import requests
import jsonschema
from src.utils.logger import get_logger

logger = get_logger("schema_assertions")


def assert_schema_valid(response: requests.Response, schema: Dict[str, Any]) -> None:
    """Validate response body against JSON schema."""
    body = response.json()
    try:
        jsonschema.validate(instance=body, schema=schema)
        logger.debug("Schema validation passed")
    except jsonschema.ValidationError as e:
        raise AssertionError(
            f"Response schema validation failed: {e.message}\n"
            f"Response: {body}"
        )


def assert_schema_has_required_fields(response: requests.Response, fields: list) -> None:
    """Assert response has all required fields."""
    body = response.json()
    missing = [f for f in fields if f not in body]
    assert not missing, \
        f"Response missing required fields: {missing}. Got: {body}"
    logger.debug(f"Assertion passed: response has all required fields")
