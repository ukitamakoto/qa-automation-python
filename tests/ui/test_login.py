import pytest
from playwright.sync_api import Page, expect

import config
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def test_valid_credentials_open_the_inventory(page: Page):
    LoginPage(page).open().login("standard_user")
    expect(page).to_have_url(InventoryPage.URL)
    expect(InventoryPage(page).title).to_have_text("Products")


@pytest.mark.parametrize(
    ("username", "password", "message"),
    [
        ("locked_out_user", config.SAUCE_PASSWORD, "Epic sadface: Sorry, this user has been locked out."),
        (
            "standard_user",
            "wrong_password",
            "Epic sadface: Username and password do not match any user in this service",
        ),
        ("", "", "Epic sadface: Username is required"),
        ("standard_user", "", "Epic sadface: Password is required"),
    ],
    ids=["locked-out-user", "wrong-password", "empty-username", "empty-password"],
)
def test_invalid_login_shows_the_right_error(page: Page, username, password, message):
    login = LoginPage(page).open()
    login.login(username, password)
    expect(login.error).to_have_text(message)
    expect(page).not_to_have_url(InventoryPage.URL)
