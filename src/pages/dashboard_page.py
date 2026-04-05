"""
Dashboard page object.
"""

from playwright.async_api import Page
from src.pages.base_page import BasePage
from src.utils.logger import get_logger

logger = get_logger("dashboard_page")


class DashboardPage(BasePage):
    """Page object for dashboard page."""
    
    # Selectors
    SUBMIT_FORM_LINK = 'a[href*="/form"]'
    EXPORT_LINK = 'a[href*="/export"]'
    LOGOUT_LINK = 'a[href*="/logout"]'
    WELCOME_TEXT = ".header"
    
    async def navigate(self) -> None:
        """Navigate to dashboard."""
        await self.goto("/dashboard")
        await self.is_visible(self.SUBMIT_FORM_LINK)
    
    async def click_submit_form(self) -> None:
        """Click on Submit Form link."""
        logger.info("Clicking Submit Form link")
        await self.click(self.SUBMIT_FORM_LINK)
        await self.page.wait_for_load_state("networkidle")
    
    async def click_export(self) -> None:
        """Click on Export Report link."""
        logger.info("Clicking Export Report link")
        await self.click(self.EXPORT_LINK)
        await self.page.wait_for_load_state("networkidle")
    
    async def click_logout(self) -> None:
        """Click on Logout link."""
        logger.info("Clicking Logout link")
        await self.click(self.LOGOUT_LINK)
        await self.page.wait_for_load_state("networkidle")
    
    async def is_dashboard_loaded(self) -> bool:
        """Check if dashboard is loaded."""
        return await self.is_visible(self.SUBMIT_FORM_LINK)
