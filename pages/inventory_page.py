import re

from playwright.sync_api import Page


class InventoryPage:
    URL = re.compile(r".*/inventory\.html$")

    def __init__(self, page: Page):
        self.page = page
        self.title = page.locator('[data-test="title"]')
        self.names = page.locator('[data-test="inventory-item-name"]')

    def wait_loaded(self) -> None:
        self.names.first.wait_for()
