from decimal import Decimal

import pytest
from playwright.sync_api import Page, expect

ALL_PRODUCTS = [
    "Sauce Labs Backpack",
    "Sauce Labs Bike Light",
    "Sauce Labs Bolt T-Shirt",
    "Sauce Labs Fleece Jacket",
    "Sauce Labs Onesie",
    "Test.allTheThings() T-Shirt (Red)",
]


@pytest.mark.parametrize(
    ("option", "key", "reverse"),
    [("za", "name", True), ("lohi", "price", False), ("hilo", "price", True)],
)
def test_sorting_orders_the_products(login_as, option, key, reverse):
    inventory = login_as("standard_user")
    names, prices = inventory.product_names(), inventory.product_prices()
    inventory.sort_by(option)
    if key == "name":
        expect(inventory.names).to_have_text(sorted(names, reverse=reverse))
    else:
        expect(inventory.prices).to_have_text([f"${p:.2f}" for p in sorted(prices, reverse=reverse)])


def test_cart_badge_follows_adds_and_removes(login_as):
    inventory = login_as("standard_user")
    expect(inventory.badge).to_have_count(0)
    inventory.add("Sauce Labs Backpack")
    inventory.add("Sauce Labs Bike Light")
    expect(inventory.badge).to_have_text("2")
    inventory.remove("Sauce Labs Bike Light")
    expect(inventory.badge).to_have_text("1")
    inventory.remove("Sauce Labs Backpack")
    expect(inventory.badge).to_have_count(0)


@pytest.mark.xfail(reason="BUG-002: problem_user sees the same image for every product")
def test_problem_user_sees_a_different_image_for_each_product(login_as):
    sources = login_as("problem_user").image_sources()
    assert len(set(sources)) == len(sources) == len(ALL_PRODUCTS)


@pytest.mark.parametrize("user", ["problem_user", "error_user"])
@pytest.mark.xfail(reason="BUG-003: Add to cart does nothing for 3 of the 6 products")
def test_every_product_can_be_added_to_the_cart(login_as, user):
    inventory = login_as(user)
    for name in ALL_PRODUCTS:
        inventory.add(name)
    expect(inventory.badge).to_have_text(str(len(ALL_PRODUCTS)), timeout=2000)


@pytest.mark.xfail(
    reason="BUG-005: error_user gets a 'Sorting is broken!' alert and the order does not change"
)
def test_error_user_can_sort_without_an_error_alert(login_as, dialogs):
    inventory = login_as("error_user")
    names = inventory.product_names()
    inventory.sort_by("za")
    expect(inventory.names).to_have_text(sorted(names, reverse=True), timeout=2000)
    assert dialogs == []


@pytest.mark.xfail(
    reason="BUG-008: visual_user sees listing prices that differ from the price charged in the cart"
)
def test_visual_user_listing_price_matches_the_cart(login_as, page: Page):
    inventory = login_as("visual_user")
    listed = inventory.price_of("Sauce Labs Backpack")
    inventory.add("Sauce Labs Backpack")
    inventory.go_to_cart()
    charged = Decimal(page.locator('[data-test="inventory-item-price"]').inner_text().lstrip("$"))
    assert charged == listed
