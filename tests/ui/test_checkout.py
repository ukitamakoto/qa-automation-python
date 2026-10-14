from decimal import ROUND_HALF_UP, Decimal

import pytest
from playwright.sync_api import Page, expect

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from tests.ui.test_inventory import ALL_PRODUCTS

CENT = Decimal("0.01")
FIVE = ALL_PRODUCTS[:5]  # every product except the red T-shirt; their item total is $113.95


def to_checkout(login_as, page: Page, user: str, products: list[str]) -> CheckoutPage:
    inventory = login_as(user)
    for name in products:
        inventory.add(name)
    inventory.go_to_cart()
    CartPage(page).checkout()
    return CheckoutPage(page)


def test_standard_user_buys_a_product_end_to_end(login_as, page: Page):
    checkout = to_checkout(login_as, page, "standard_user", ["Sauce Labs Backpack"])
    checkout.submit()
    expect(page).to_have_url(CheckoutPage.STEP_TWO)
    assert checkout.summary() == {"item_total": "29.99", "tax": "2.40", "total": "32.39"}
    checkout.finish()
    expect(page).to_have_url(CheckoutPage.COMPLETE)
    expect(checkout.complete_header).to_have_text("Thank you for your order!")


@pytest.mark.parametrize(
    ("missing", "message"),
    [
        ("first", "Error: First Name is required"),
        ("last", "Error: Last Name is required"),
        ("postal", "Error: Postal Code is required"),
    ],
)
def test_checkout_requires_each_field(login_as, page: Page, missing, message):
    checkout = to_checkout(login_as, page, "standard_user", ["Sauce Labs Onesie"])
    data = {"first": "Ana", "last": "Silva", "postal": "8000-123"} | {missing: ""}
    checkout.submit(data["first"], data["last"], data["postal"])
    expect(checkout.error).to_have_text(message)
    expect(page).not_to_have_url(CheckoutPage.STEP_TWO)


def test_order_total_is_items_plus_8_percent_tax(login_as, page: Page):
    inventory = login_as("standard_user")
    items = sum(inventory.price_of(p) for p in ALL_PRODUCTS)
    tax = (items * Decimal("0.08")).quantize(CENT, ROUND_HALF_UP)
    for name in ALL_PRODUCTS:
        inventory.add(name)
    inventory.go_to_cart()
    CartPage(page).checkout()
    checkout = CheckoutPage(page)
    checkout.submit()
    assert checkout.summary() == {
        "item_total": f"{items:.2f}",
        "tax": f"{tax:.2f}",
        "total": f"{items + tax:.2f}",
    }


@pytest.mark.xfail(
    reason="BUG-001: Item total shows floating-point noise ($113.94999999999999) for some add orders"
)
def test_item_total_is_rounded_to_cents_whatever_the_add_order(login_as, page: Page):
    checkout = to_checkout(login_as, page, "standard_user", list(reversed(FIVE)))
    checkout.submit()
    assert checkout.summary()["item_total"] == "113.95"


@pytest.mark.xfail(reason="BUG-004: for problem_user, typing in Last Name overwrites First Name")
def test_problem_user_can_fill_the_checkout_form(login_as, page: Page):
    checkout = to_checkout(login_as, page, "problem_user", ["Sauce Labs Backpack"])
    checkout.fill("Ana", "Silva", "8000-123")
    expect(checkout.first_name).to_have_value("Ana", timeout=2000)
    expect(checkout.last_name).to_have_value("Silva", timeout=2000)


@pytest.mark.xfail(
    reason="BUG-006: for error_user, Last Name ignores typing and checkout continues without it"
)
def test_error_user_checkout_keeps_the_last_name(login_as, page: Page):
    checkout = to_checkout(login_as, page, "error_user", ["Sauce Labs Backpack"])
    checkout.fill("Ana", "Silva", "8000-123")
    expect(checkout.last_name).to_have_value("Silva", timeout=2000)


@pytest.mark.xfail(reason="BUG-007: for error_user, Finish does not complete the order")
def test_error_user_can_finish_the_order(login_as, page: Page):
    checkout = to_checkout(login_as, page, "error_user", ["Sauce Labs Backpack"])
    checkout.submit()
    expect(page).to_have_url(CheckoutPage.STEP_TWO)
    checkout.finish()
    expect(page).to_have_url(CheckoutPage.COMPLETE, timeout=3000)
