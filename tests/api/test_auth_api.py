"""
API tests for authentication endpoints.
"""

import pytest
from src.api.schemas.auth_schema import AUTH_LOGIN_RESPONSE_SCHEMA
from src.api.assertions.response_assertions import (
    assert_status_code,
    assert_json_field_equals,
)
from src.api.assertions.schema_assertions import assert_schema_valid


@pytest.mark.api
@pytest.mark.smoke
def test_api_login_valid_credentials(auth_client):
    """Test API login with valid credentials."""
    result = auth_client.login("testuser@example.com", "password123")

    assert_status_code(result["response"], 200)
    assert_json_field_equals(result["response"], "success", True)
    assert_schema_valid(result["response"], AUTH_LOGIN_RESPONSE_SCHEMA)


@pytest.mark.api
def test_api_login_invalid_credentials(auth_client):
    """Test API login with invalid credentials returns 401."""
    result = auth_client.login("testuser@example.com", "wrongpassword")

    assert_status_code(result["response"], 401)
    assert "error" in result["body"]


@pytest.mark.api
def test_api_login_missing_email(auth_client):
    """Test API login with missing email returns 400."""
    result = auth_client.login("", "password123")

    assert_status_code(result["response"], 400)


@pytest.mark.api
def test_api_list_users(users_client):
    """Test API endpoint to list users."""
    result = users_client.list_users()

    assert_status_code(result["response"], 200)
    body = result["body"]
    assert "users" in body
    assert isinstance(body["users"], list)
    assert len(body["users"]) > 0
