"""
UI tests for login functionality.
"""

import pytest


@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.asyncio
async def test_login_with_valid_credentials(login_page):
    """Test login with valid credentials."""
    await login_page.navigate()
    await login_page.login("testuser@example.com", "password123")
    
    # After login, we should be on the dashboard
    current_url = await login_page.get_url()
    assert "/dashboard" in current_url or "dashboard" in current_url


@pytest.mark.ui
@pytest.mark.asyncio
async def test_login_with_invalid_credentials(login_page):
    """Test login with invalid credentials shows error."""
    await login_page.navigate()
    await login_page.login("testuser@example.com", "wrongpassword")
    
    # Error message should be displayed
    error = await login_page.get_error_message()
    assert error
    assert "Invalid email or password" in error


@pytest.mark.ui
@pytest.mark.asyncio
async def test_login_page_title(login_page):
    """Test login page has correct title."""
    await login_page.navigate()
    title = await login_page.get_title()
    assert "Login" in title
