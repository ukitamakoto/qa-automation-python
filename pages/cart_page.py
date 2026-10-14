from playwright.sync_api import Page


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.item_names = page.locator('[data-test="inventory-item-name"]')
        self.checkout_button = page.locator('[data-test="checkout"]')

    def names(self) -> list[str]:
        return self.item_names.all_inner_texts()

    def checkout(self) -> None:
        self.checkout_button.click()
