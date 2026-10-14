import re

from playwright.sync_api import Page


def money(label: str) -> str:
    """'Item total: $29.99' -> '29.99'. Kept as text so formatting defects stay visible."""
    return label.split("$", 1)[1].strip()


class CheckoutPage:
    STEP_TWO = re.compile(r".*/checkout-step-two\.html$")
    COMPLETE = re.compile(r".*/checkout-complete\.html$")

    def __init__(self, page: Page):
        self.page = page
        self.first_name = page.locator('[data-test="firstName"]')
        self.last_name = page.locator('[data-test="lastName"]')
        self.postal_code = page.locator('[data-test="postalCode"]')
        self.continue_button = page.locator('[data-test="continue"]')
        self.error = page.locator('[data-test="error"]')
        self.subtotal = page.locator('[data-test="subtotal-label"]')
        self.tax = page.locator('[data-test="tax-label"]')
        self.total = page.locator('[data-test="total-label"]')
        self.finish_button = page.locator('[data-test="finish"]')
        self.complete_header = page.locator('[data-test="complete-header"]')

    def fill(self, first: str, last: str, postal: str) -> None:
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(postal)

    def submit(self, first: str = "Ana", last: str = "Silva", postal: str = "8000-123") -> None:
        self.fill(first, last, postal)
        self.continue_button.click()

    def summary(self) -> dict[str, str]:
        return {
            "item_total": money(self.subtotal.inner_text()),
            "tax": money(self.tax.inner_text()),
            "total": money(self.total.inner_text()),
        }

    def finish(self) -> None:
        self.finish_button.click()
