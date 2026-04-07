"""
UI tests for dashboard navigation and export flow.
"""

from pathlib import Path

import pytest


def get_export_file_path():
    """Get the export file path."""
    return Path(__file__).parent.parent.parent / "reports" / "export.csv"


async def login_as_default_user(login_page):
    """Log in with the seeded user credentials."""
    await login_page.navigate()
    await login_page.login("testuser@example.com", "password123")


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.asyncio
async def test_dashboard_navigation_to_form(login_page, dashboard_page):
    """Test dashboard navigation to the form page."""
    await login_as_default_user(login_page)

    await dashboard_page.click_submit_form()

    current_url = await dashboard_page.get_url()
    assert current_url.endswith("/form")
    assert "Submit Form" in await dashboard_page.get_title()


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.asyncio
async def test_dashboard_export_link_generates_report(login_page, dashboard_page):
    """Test dashboard export navigation generates the report page and file."""
    export_path = get_export_file_path()
    if export_path.exists():
        export_path.unlink()

    await login_as_default_user(login_page)

    await dashboard_page.click_export()

    current_url = await dashboard_page.get_url()
    page_text = await dashboard_page.get_text("body")

    assert current_url.endswith("/export")
    assert "Export generated successfully" in page_text
    assert export_path.exists()
