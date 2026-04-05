"""
Form submission page object.
"""

from playwright.async_api import Page
from src.pages.base_page import BasePage
from src.utils.logger import get_logger

logger = get_logger("form_page")


class FormPage(BasePage):
    """Page object for form submission page."""
    
    # Selectors
    NAME_INPUT = "input[name='name']"
    EMAIL_INPUT = "input[name='email']"
    MESSAGE_INPUT = "textarea[name='message']"
    SUBMIT_BUTTON = "button[type='submit']"
    SUCCESS_MESSAGE = ".success"
    ERROR_MESSAGE = ".error"
    BACK_LINK = "a"  # Back to Dashboard link
    
    async def navigate(self) -> None:
        """Navigate to form page."""
        await self.goto("/form")
        await self.is_visible(self.NAME_INPUT)
    
    async def submit_form(self, name: str, email: str, message: str) -> None:
        """Submit form with provided data."""
        logger.info(f"Submitting form with name: {name}")
        await self.fill_input(self.NAME_INPUT, name)
        await self.fill_input(self.EMAIL_INPUT, email)
        await self.fill_input(self.MESSAGE_INPUT, message)
        await self.click(self.SUBMIT_BUTTON)
        await self.page.wait_for_load_state("networkidle")
    
    async def get_success_message(self) -> str:
        """Get success message."""
        if await self.is_visible(self.SUCCESS_MESSAGE):
            return await self.get_text(self.SUCCESS_MESSAGE)
        return ""
    
    async def is_success_displayed(self) -> bool:
        """Check if success message is displayed."""
        return await self.is_visible(self.SUCCESS_MESSAGE)
    
    async def get_error_message(self) -> str:
        """Get error message."""
        if await self.is_visible(self.ERROR_MESSAGE):
            return await self.get_text(self.ERROR_MESSAGE)
        return ""
    
    async def is_error_displayed(self) -> bool:
        """Check if error message is displayed."""
        return await self.is_visible(self.ERROR_MESSAGE)
