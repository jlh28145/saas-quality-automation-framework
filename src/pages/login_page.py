"""
Login page object.
"""

from playwright.async_api import Page
from src.pages.base_page import BasePage
from src.utils.logger import get_logger

logger = get_logger("login_page")


class LoginPage(BasePage):
    """Page object for login page."""
    
    # Selectors
    EMAIL_INPUT = "input[name='email']"
    PASSWORD_INPUT = "input[name='password']"
    SUBMIT_BUTTON = "button[type='submit']"
    ERROR_MESSAGE = ".error"
    
    async def navigate(self) -> None:
        """Navigate to login page."""
        await self.goto("/login")
        await self.is_visible(self.EMAIL_INPUT)
    
    async def login(self, email: str, password: str) -> None:
        """Perform login."""
        logger.info(f"Logging in with email: {email}")
        await self.fill_input(self.EMAIL_INPUT, email)
        await self.fill_input(self.PASSWORD_INPUT, password)
        await self.click(self.SUBMIT_BUTTON)
        await self.page.wait_for_load_state("networkidle")
    
    async def get_error_message(self) -> str:
        """Get error message if login fails."""
        if await self.is_visible(self.ERROR_MESSAGE):
            return await self.get_text(self.ERROR_MESSAGE)
        return ""
    
    async def is_error_displayed(self) -> bool:
        """Check if error message is displayed."""
        return await self.is_visible(self.ERROR_MESSAGE)
