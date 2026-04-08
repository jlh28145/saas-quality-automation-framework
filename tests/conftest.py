"""
Pytest configuration and fixtures.
"""

import asyncio
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import pytest
import requests
from faker import Faker
from playwright.async_api import async_playwright

from src.utils.config import get_config, reset_config
from src.utils.logger import get_logger
from src.pages.login_page import LoginPage
from src.pages.dashboard_page import DashboardPage
from src.pages.form_page import FormPage
from src.api.clients.auth_client import AuthClient
from src.api.clients.forms_client import FormsClient
from src.api.clients.exports_client import ExportsClient
from src.api.clients.users_client import UsersClient

logger = get_logger(__name__, log_dir=Path(__file__).parent.parent / "reports" / "logs")
SCREENSHOT_DIR = Path(__file__).parent.parent / "reports" / "screenshots"
DEFAULT_FAKE_DATA_SEED = 20260407


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach test phase reports to the test item for fixture teardown handling."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture
def config():
    """Get test configuration."""
    reset_config()
    return get_config()


@pytest.fixture
def fake_data_seed():
    """Provide a stable seed for opt-in data-variation tests."""
    return int(os.getenv("FAKE_DATA_SEED", DEFAULT_FAKE_DATA_SEED))


@pytest.fixture
def fake_data(fake_data_seed):
    """Provide a seeded Faker instance for reproducible randomized inputs."""
    Faker.seed(fake_data_seed)
    fake = Faker()
    fake.seed_instance(fake_data_seed)
    logger.info(f"Using Faker seed: {fake_data_seed}")
    return fake


@pytest.fixture(scope="session", autouse=True)
def app_server():
    """Start the Flask app for the test session."""
    config = get_config()
    base_url = config.get("base_url")
    app_path = Path(__file__).parent.parent / "app" / "main.py"
    env = os.environ.copy()
    env.setdefault("ENV", config.environment)

    process = subprocess.Popen(
        [sys.executable, str(app_path)],
        cwd=Path(__file__).parent.parent,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    deadline = time.time() + 15
    last_error = None
    while time.time() < deadline:
        if process.poll() is not None:
            raise RuntimeError("Flask app exited before the test session started")
        try:
            response = requests.get(f"{base_url}/login", timeout=1)
            if response.ok:
                break
        except requests.RequestException as exc:
            last_error = exc
            time.sleep(0.25)
    else:
        process.terminate()
        process.wait(timeout=5)
        raise RuntimeError(f"Flask app did not become ready in time: {last_error}")

    yield

    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


@pytest.fixture
async def browser(config, app_server):
    """Create Playwright browser instance."""
    async with async_playwright() as p:
        browser_name = os.getenv("BROWSER", config.get("browser", "chromium"))
        browser_type = getattr(p, browser_name, None)
        if browser_type is None:
            raise ValueError(f"Unsupported Playwright browser: {browser_name}")

        browser = await browser_type.launch(
            headless=config.get("headless", True),
            slow_mo=config.get("slow_mo", 0),
        )
        yield browser
        await browser.close()


@pytest.fixture
async def page(browser, config, request):
    """Create Playwright page instance."""
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    page = await browser.new_page()
    page.set_default_timeout(config.get("timeout", 5000))
    yield page
    if config.get("screenshot_on_failure", False):
        call_report = getattr(request.node, "rep_call", None)
        if call_report and call_report.failed:
            safe_name = re.sub(r"[^A-Za-z0-9._-]+", "_", request.node.nodeid)
            screenshot_path = SCREENSHOT_DIR / f"{safe_name}.png"
            await page.screenshot(path=str(screenshot_path), full_page=True)
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
