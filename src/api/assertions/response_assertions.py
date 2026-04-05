"""
Response status and content assertions.
"""

from typing import Any, Dict
import requests
from src.utils.logger import get_logger

logger = get_logger("response_assertions")


def assert_status_code(response: requests.Response, expected: int) -> None:
    """Assert response status code."""
    logger.info(f"Asserting status code: {response.status_code} == {expected}")
    assert response.status_code == expected, \
        f"Expected status {expected}, got {response.status_code}. Body: {response.text}"


def assert_status_ok(response: requests.Response) -> None:
    """Assert response is success (2xx)."""
    assert_status_code(response, 200)


def assert_status_created(response: requests.Response) -> None:
    """Assert response status is 201 Created."""
    assert_status_code(response, 201)


def assert_status_bad_request(response: requests.Response) -> None:
    """Assert response status is 400 Bad Request."""
    assert_status_code(response, 400)


def assert_status_unauthorized(response: requests.Response) -> None:
    """Assert response status is 401 Unauthorized."""
    assert_status_code(response, 401)


def assert_json_body_contains(response: requests.Response, key: str, value: Any = None) -> None:
    """Assert JSON body contains key (and optionally matches value)."""
    body = response.json()
    assert key in body, f"Key '{key}' not found in response body: {body}"
    if value is not None:
        assert body[key] == value, \
            f"Expected {key}={value}, got {key}={body[key]}"
    logger.debug(f"Assertion passed: {key} in response body")


def assert_json_field_equals(response: requests.Response, key: str, expected: Any) -> None:
    """Assert JSON field equals expected value."""
    body = response.json()
    actual = body.get(key)
    assert actual == expected, \
        f"Expected {key}={expected}, got {actual}"
    logger.debug(f"Assertion passed: {key} == {expected}")


def assert_json_field_is_type(response: requests.Response, key: str, expected_type: type) -> None:
    """Assert JSON field is of expected type."""
    body = response.json()
    actual = body.get(key)
    assert isinstance(actual, expected_type), \
        f"Expected {key} to be {expected_type.__name__}, got {type(actual).__name__}"
    logger.debug(f"Assertion passed: {key} is {expected_type.__name__}")
