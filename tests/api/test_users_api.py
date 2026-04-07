"""
API tests for user endpoints.
"""

import pytest

from src.api.assertions.response_assertions import (
    assert_json_field_is_type,
    assert_status_code,
)
from src.api.assertions.schema_assertions import assert_schema_valid
from src.api.schemas.user_schema import USERS_LIST_RESPONSE_SCHEMA


@pytest.mark.api
@pytest.mark.regression
def test_api_list_users_returns_schema_valid_response(users_client):
    """Test the users endpoint returns the expected schema."""
    result = users_client.list_users()

    assert_status_code(result["response"], 200)
    assert_schema_valid(result["response"], USERS_LIST_RESPONSE_SCHEMA)
    assert_json_field_is_type(result["response"], "users", list)


@pytest.mark.api
def test_api_list_users_contains_seeded_accounts(users_client):
    """Test the users endpoint returns the seeded users."""
    result = users_client.list_users()

    assert_status_code(result["response"], 200)
    users = result["body"]["users"]
    emails = {user["email"] for user in users}

    assert "testuser@example.com" in emails
    assert "admin@example.com" in emails
