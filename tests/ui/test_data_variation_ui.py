"""
Opt-in UI tests that use seeded Faker data for broader input coverage.

The main UI suite remains deterministic; these tests are supplemental and
reproducible through the logged Faker seed.
"""

import pytest


async def login_as_default_user(login_page):
    """Log in with the seeded user credentials."""
    await login_page.navigate()
    await login_page.login("testuser@example.com", "password123")


@pytest.mark.ui
@pytest.mark.data_variation
@pytest.mark.asyncio
async def test_ui_form_submission_accepts_seeded_faker_data(login_page, form_page, fake_data, fake_data_seed):
    """Submit a valid seeded Faker payload through the UI."""
    await login_as_default_user(login_page)
    await form_page.navigate()

    await form_page.submit_form(
        fake_data.name(),
        fake_data.email(),
        f"{fake_data.sentence(nb_words=9)} Seed:{fake_data_seed}",
    )

    assert await form_page.is_success_displayed()
