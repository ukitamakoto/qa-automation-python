import re
from decimal import Decimal

from playwright.sync_api import Page


def slug(product_name: str) -> str:
    """'Sauce Labs Bike Light' -> 'sauce-labs-bike-light' (the suffix of the app's data-test ids)."""
    return product_name.lower().replace(" ", "-")


class InventoryPage:
    URL = re.compile(r".*/inventory\.html$")

    def __init__(self, page: Page):
        self.page = page
        self.title = page.locator('[data-test="title"]')
        self.items = page.locator('[data-test="inventory-item"]')
        self.names = page.locator('[data-test="inventory-item-name"]')
        self.prices = page.locator('[data-test="inventory-item-price"]')
        self.images = page.locator('[data-test="inventory-item"] img')
        self.sort = page.locator('[data-test="product-sort-container"]')
        self.badge = page.locator('[data-test="shopping-cart-badge"]')
        self.cart_link = page.locator('[data-test="shopping-cart-link"]')

    def wait_loaded(self) -> None:
        self.names.first.wait_for()

    def product_names(self) -> list[str]:
        return self.names.all_inner_texts()

    def product_prices(self) -> list[Decimal]:
        return [Decimal(p.lstrip("$")) for p in self.prices.all_inner_texts()]

    def price_of(self, name: str) -> Decimal:
        item = self.items.filter(has=self.page.get_by_text(name, exact=True))
        return Decimal(item.locator('[data-test="inventory-item-price"]').inner_text().lstrip("$"))

    def sort_by(self, option: str) -> None:
        self.sort.select_option(option)

    def add(self, name: str) -> None:
        self.page.locator(f'[data-test="add-to-cart-{slug(name)}"]').click()

    def remove(self, name: str) -> None:
        self.page.locator(f'[data-test="remove-{slug(name)}"]').click()

    def image_sources(self) -> list[str]:
        self.images.first.wait_for()
        return [img.get_attribute("src") or "" for img in self.images.all()]

    def go_to_cart(self) -> None:
        self.cart_link.click()
        # The app is a SPA: the URL changes before the cart replaces the inventory DOM.
        self.page.locator('[data-test="checkout"]').wait_for()
