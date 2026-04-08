"""
UI tests for form submission behavior.
"""

import pytest


async def login_as_default_user(login_page):
    """Log in with the seeded user credentials."""
    await login_page.navigate()
    await login_page.login("testuser@example.com", "password123")


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.asyncio
async def test_form_submission_with_valid_data(login_page, form_page):
    """Test a successful form submission from the UI."""
    await login_as_default_user(login_page)
    await form_page.navigate()

    await form_page.submit_form(
        "UI Test User",
        "ui@example.com",
        "This is a valid UI form submission message.",
    )

    assert await form_page.is_success_displayed()
    assert "Form submitted successfully" in await form_page.get_success_message()


@pytest.mark.ui
@pytest.mark.asyncio
async def test_form_submission_with_short_message_shows_validation_error(
    login_page, form_page
):
    """Test validation feedback for an invalid form submission."""
    await login_as_default_user(login_page)
    await form_page.navigate()

    await form_page.submit_form("UI Test User", "ui@example.com", "short")

    assert await form_page.is_error_displayed()
    assert (
        "Message must be at least 10 characters" in await form_page.get_error_message()
    )
