import pytest
from playwright.sync_api import Page, expect

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@pytest.fixture
def login_as(page: Page):
    """Log in as a SauceDemo user and return the loaded inventory page."""

    def _login(username: str) -> InventoryPage:
        LoginPage(page).open().login(username)
        expect(page).to_have_url(InventoryPage.URL)
        inventory = InventoryPage(page)
        inventory.wait_loaded()
        return inventory

    return _login


@pytest.fixture
def dialogs(page: Page) -> list[str]:
    """Collect (and accept) every JavaScript dialog the page opens."""
    messages: list[str] = []
    page.on("dialog", lambda d: (messages.append(d.message), d.accept()))
    return messages
