"""
Pytest configuration and fixtures.
"""

import asyncio
import pytest
from pathlib import Path
from playwright.async_api import async_playwright

from src.utils.config import get_config
from src.utils.logger import get_logger
from src.pages.login_page import LoginPage
from src.pages.dashboard_page import DashboardPage
from src.pages.form_page import FormPage
from src.api.clients.auth_client import AuthClient
from src.api.clients.forms_client import FormsClient
from src.api.clients.exports_client import ExportsClient
from src.api.clients.users_client import UsersClient


logger = get_logger(__name__, log_dir=Path(__file__).parent.parent / "reports" / "logs")


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def config():
    """Get test configuration."""
    return get_config("dev")


@pytest.fixture
async def browser():
    """Create Playwright browser instance."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        yield browser
        await browser.close()


@pytest.fixture
async def page(browser):
    """Create Playwright page instance."""
    page = await browser.new_page()
    yield page
    await page.close()


@pytest.fixture
async def login_page(page, config):
    """Create LoginPage instance."""
    return LoginPage(page, config.get("base_url"))


@pytest.fixture
async def dashboard_page(page, config):
    """Create DashboardPage instance."""
    return DashboardPage(page, config.get("base_url"))


@pytest.fixture
async def form_page(page, config):
    """Create FormPage instance."""
    return FormPage(page, config.get("base_url"))


@pytest.fixture
def auth_client(config):
    """Create AuthClient instance."""
    client = AuthClient(config.get("api_base_url"))
    yield client
    client.close()


@pytest.fixture
def forms_client(config):
    """Create FormsClient instance."""
    client = FormsClient(config.get("api_base_url"))
    yield client
    client.close()


@pytest.fixture
def exports_client(config):
    """Create ExportsClient instance."""
    client = ExportsClient(config.get("api_base_url"))
    yield client
    client.close()


@pytest.fixture
def users_client(config):
    """Create UsersClient instance."""
    client = UsersClient(config.get("api_base_url"))
    yield client
    client.close()
