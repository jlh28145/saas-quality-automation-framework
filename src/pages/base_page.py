"""
Base page class with common page object methods.
"""

from playwright.async_api import Page
from src.utils.logger import get_logger

logger = get_logger("pages")


class BasePage:
    """Base class for all page objects."""

    def __init__(self, page: Page, base_url: str = "http://localhost:5000"):
        """Initialize page object."""
        self.page = page
        self.base_url = base_url

    async def goto(self, path: str) -> None:
        """Navigate to a path."""
        url = f"{self.base_url}{path}"
        logger.debug(f"Navigating to {url}")
        await self.page.goto(url)

    async def fill_input(self, selector: str, value: str) -> None:
        """Fill an input field."""
        logger.debug(f"Filling {selector} with value")
        await self.page.fill(selector, value)

    async def click(self, selector: str) -> None:
        """Click an element."""
        logger.debug(f"Clicking {selector}")
        await self.page.click(selector)

    async def get_text(self, selector: str) -> str:
        """Get text content of an element."""
        text = await self.page.text_content(selector)
        return text or ""

    async def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        """Check if element is visible."""
        try:
            await self.page.wait_for_selector(
                selector, timeout=timeout, state="visible"
            )
            return True
        except Exception:
            return False

    async def wait_for_navigation(self) -> None:
        """Wait for page navigation to complete."""
        await self.page.wait_for_load_state("networkidle")

    async def get_title(self) -> str:
        """Get page title."""
        return await self.page.title()

    async def get_url(self) -> str:
        """Get current URL."""
        return self.page.url
